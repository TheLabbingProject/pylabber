"""
Definition of the :class:`ExportDestination` class.
"""
from pathlib import Path
from typing import Iterable, Union

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
            self.transport.connect(
                self.key, self.username, self.password,
            )

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

            # Create parents if necessary.
            if create_parents:
                parents = []
                for part in relative_path.parts[:-1]:
                    parents.append(part)
                    current = "/".join(parents)
                    try:
                        self.sftp_client.mkdir(current)
                    except OSError:
                        pass

            # Copy file.
            self.sftp_client.put(str(path), str(relative_path))
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
