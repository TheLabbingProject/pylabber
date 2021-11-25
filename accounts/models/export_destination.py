"""
Definition of the :class:`ExportDestination` class.
"""
import logging
from pathlib import Path
from typing import Iterable, Union
from paramiko import SSHException

import paramiko
from accounts.models.utils.ssh import get_known_hosts
from django.conf import settings
from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from mirage import fields


class ExportDestination(TitleDescriptionModel):
    """
    Some SSH reachable destination for file export.
    """

    #: SSH destination host IP.
    ip = models.GenericIPAddressField(
        blank=False, null=False, verbose_name="IP"
    )

    #: Authentication username.
    username = models.CharField(max_length=128, blank=False, null=False)

    #: Authentication password.
    password = fields.EncryptedCharField(
        max_length=128, blank=False, null=False
    )

    #: Destination in the host filesystem.
    destination = models.CharField(max_length=512, blank=False, null=False)

    #: Users that may export to this destination.
    users = models.ManyToManyField("accounts.User")

    #: Port to use for SSH connection.
    PORT: int = 22

    #: Default SSH connection banner timeout value.
    BANNER_TIMEOUT: int = 200

    # Host key cache.
    _key = None
    # Transport instance cache.
    _transport = None
    # SFTPClient cache.
    _sftp_client = None

    _logger = logging.getLogger("accounts.export_destination")

    def __str__(self) -> str:
        return f"{self.username}@{self.ip}"

    def get_key(self) -> paramiko.ecdsakey.ECDSAKey:
        """
        Returns the key of the host if it exists within the *known_hosts* file.

        See Also
        --------
        * :meth:`key`

        Returns
        -------
        paramiko.ecdsakey.ECDSAKey
            Host key
        """
        try:
            key_dict = get_known_hosts()[self.ip]
        except KeyError:
            pass
        else:
            key_type = key_dict.keys()[0]
            return key_dict[key_type]

    def create_transport(
        self, banner_timeout: int = None
    ) -> paramiko.Transport:
        """
        Returns the transport instance which will be used to negotiate the
        connection.

        Parameters
        ----------
        banner_timeout : int
            Timeout in seconds protocol banner read

        See Also
        --------
        :meth:`transport`

        Returns
        -------
        paramiko.Transport
            SSH transport thread
        """
        transport = paramiko.Transport((self.ip, self.PORT))
        transport.banner_timeout = (
            self.BANNER_TIMEOUT if banner_timeout is None else banner_timeout
        )
        return transport

    def connect(self) -> None:
        """
        Negotiates a connection with the host.
        """
        if not self.transport.active:
            if self.key is not None:
                self.transport._preferred_keys = [self.key.get_name()]
            self.transport.start_client(timeout=3)
            remote_key = self.transport.get_remote_server_key()
            remote_name = remote_key.get_name()
            remote_bytes = remote_key.asbytes()
            expected_name = self.key.get_name()
            expected_bytes = self.key.asbytes()
            valid_name = remote_name == expected_name
            valid_bytes = remote_bytes == expected_bytes
            if not (valid_name and valid_bytes):
                self._logger.warn("Bad host key from server!")
                self._logger.warn(
                    f"Expected: {self.hostkey.get_name()}: {repr(self.key.asbytes())}"  # noqa: E501
                )
                self._logger.warn(
                    f"Got     : {remote_key.get_name()}: {repr(remote_key.asbytes())}"  # noqa: E501
                )
                raise SSHException("Bad host key from server")
            self._logger.debug(
                f"Host {self.ip} key ({expected_name}) successfully verified."
            )
            self._logger.debug("Attempting password authentication...")
            self.transport.auth_password(self.username, self.password)

    def start_sftp_client(self) -> paramiko.sftp_client.SFTPClient:
        """
        Returns an SFTP client, enabling secure interaction with the host
        filesystem.

        See Also
        --------
        * :meth:`sftp_client`

        Returns
        -------
        paramiko.sftp_client.SFTPClient
            SFTP Client connected to the host filesystem
        """
        if not self.transport.active:
            self.connect()
        return paramiko.SFTPClient.from_transport(self.transport)

    def put(
        self, path: Union[Path, Iterable[Path]], create_parents: bool = True
    ) -> None:
        """
        Copies a file from the server to this export destination. Files will
        be moved to the same location relative to the applications MEDIA_ROOT.

        Parameters
        ----------
        path : Path
            File to copy
        create_parents : bool, optional
            Whether to automatically create directory tree parents, by default
            True
        """
        if isinstance(path, (str, Path)):
            relative_path = Path(path).relative_to(settings.MEDIA_ROOT)
            self._logger.debug(f"Starting {relative_path} export to {self}...")
            # Create parents one by one.
            # (No `parents` or `exist_ok` available)
            remote_base = Path(self.destination)
            # Windows requires absolute paths, Linux requires relative.
            required_absolute = False
            if create_parents:
                self._logger.debug(
                    "Creating destination directory within the host..."
                )
                parents = []
                for part in relative_path.parts[:-1]:
                    parents.append(part)
                    current = "/".join(parents)
                    self._logger.debug(f"Trying to create {current}...")
                    absolute_parent = str(remote_base / current)
                    # Found to run on Windows in a previous iteration.
                    if required_absolute:
                        self.sftp_client.mkdir(absolute_parent)
                        self._logger.debug(
                            f"Successfully created {absolute_parent}."
                        )
                    else:
                        try:
                            self.sftp_client.mkdir(current)
                        except OSError:
                            # Handle connections to Windows.
                            self._logger.debug(
                                f"Failed to create {current} (OSError), trying with absolute path..."  # noqa: E501
                            )
                            try:
                                self.sftp_client.mkdir(absolute_parent)
                            # Directory already exists.
                            except OSError:
                                self._logger.debug(
                                    "Parent creation raised OSError for both relative and absolute paths, assuming directory exists in host."  # noqa: E501
                                )
                                pass
                            # Succeeded creating with absolute path.
                            else:
                                self._logger.debug(
                                    f"Successfully created {absolute_parent}."
                                )
                                required_absolute = True
                        else:
                            self._logger.debug(
                                f"Successfully created {current}."
                            )

            # Copy file.
            absolute_destination = str(remote_base / relative_path)
            destination = (
                absolute_destination
                if required_absolute
                else str(relative_path)
            )
            self._logger.debug(f"Copying {relative_path} to {destination}")
            try:
                self.sftp_client.put(str(path), destination)
            except OSError as first_exception:
                # In case the directory existed or an OSError was re-raised
                # in parent creation and exporting to Windows, make sure to
                # try using the absolute path.
                self._logger.debug(
                    f"Export to {destination} raised:\n{first_exception}"
                )
                if destination != absolute_destination:
                    self._logger.debug(
                        "Re-trying export with absolute host destination path."  # noqa: E501
                    )
                    self._logger.debug(
                        f"Copying {relative_path} to {absolute_destination}"
                    )
                    try:
                        self.sftp_client.put(str(path), absolute_destination)
                    except OSError as second_exception:
                        self._logger.debug(
                            f"Failed to export {relative_path} to both relative and absolute destinations in the {self}."  # noqa: E501
                        )
                        self._logger.debug(
                            f"Relative path exception:\n{first_exception}"
                        )
                        self._logger.debug(
                            f"Absolute path exception:\n{second_exception}"
                        )
                        raise
                    else:
                        self._logger.debug(
                            f"Successfully exported {relative_path} to {self}/{absolute_destination}"  # noqa: E501
                        )
            else:
                self._logger.debug(
                    f"Validating {absolute_destination} exists in {self}..."
                )
                try:
                    self.sftp_client.stat(absolute_destination)
                except FileNotFoundError:
                    self._logger.debug(
                        "Exported file could not be found in {self}!"
                    )
                    self._logger.debug(
                        "Re-trying export with absolute host destination path."  # noqa: E501
                    )
                    self._logger.debug(
                        f"Copying {relative_path} to {absolute_destination}"
                    )
                    try:
                        self.sftp_client.put(str(path), absolute_destination)
                    except OSError as e:
                        self._logger.debug(
                            f"File export to absolute destination raised:\n{e}"  # noqa: E501
                        )
                    else:
                        self._logger.debug(
                            f"Validating {absolute_destination} exists in {self}..."  # noqa: E501
                        )
                        try:
                            self.sftp_client.stat(absolute_destination)
                        except FileNotFoundError:
                            self._logger.debug(
                                "File transfter did not raise an exception, but the destination file could not be validated to have been created in {self}!"  # noqa: E501
                            )
                            raise

                else:
                    self._logger.debug(
                        f"Successfully exported {relative_path} to {self}/{destination}"  # noqa: E501
                    )
        else:
            for p in path:
                self.put(p, create_parents)

    @property
    def key(self):
        """
        Returns the key of the host if it exists within the *known_hosts* file.

        See Also
        --------
        * :meth:`get_key`

        Returns
        -------
        paramiko.ecdsakey.ECDSAKey
            Host key
        """
        if self._key is None:
            self._key = self.get_key()
        return self._key

    @property
    def transport(self):
        """
        Returns the transport instance which will be used to negotiate the
        connection.

        See Also
        --------
        :meth:`create_transport`

        Returns
        -------
        paramiko.Transport
            SSH transport thread
        """
        if self._transport is None:
            self._transport = self.create_transport()
        return self._transport

    @property
    def sftp_client(self) -> paramiko.sftp_client.SFTPClient:
        """
        Returns an SFTP client, enabling secure interaction with the host
        filesystem.

        See Also
        --------
        * :meth:`start_sftp_client`

        Returns
        -------
        paramiko.sftp_client.SFTPClient
            SFTP Client connected to the host filesystem
        """
        if self._sftp_client is None:
            self._sftp_client = self.start_sftp_client()
        return self._sftp_client
