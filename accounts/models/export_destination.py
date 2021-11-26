"""
Definition of the :class:`ExportDestination` class.
"""
import logging
from pathlib import Path
from typing import Iterable, Tuple, Union

import paramiko
from accounts.models import logs
from accounts.models.utils.ssh import get_known_hosts
from django.conf import settings
from django.db import models
from django_extensions.db.models import TitleDescriptionModel
from mirage import fields
from paramiko import SSHException
from tqdm import tqdm


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

    #: Default SSH connection banner timeout value in seconds.
    BANNER_TIMEOUT: int = 100

    #: Default socket connection timeout value in seconds.
    SOCKET_TIMEOUT: int = 3

    #: Default SSH session negotiation timeout.
    SESSION_TIMEOUT: int = 3

    # Host key cache.
    _key = None
    # Transport instance cache.
    _transport = None
    # SFTPClient cache.
    _sftp_client = None

    _logger = logging.getLogger("accounts.export_destination")

    #: String representation template.
    STRING_TEMPLATE: str = "{username}@{ip}"

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            Export destination string representation
        """
        return self.STRING_TEMPLATE.format(username=self.username, ip=self.ip)

    def get_key(self) -> paramiko.ecdsakey.ECDSAKey:
        """
        Returns the public key of the host if it exists within the
        *known_hosts* file.

        See Also
        --------
        * :meth:`key`

        Returns
        -------
        paramiko.ecdsakey.ECDSAKey
            Host key
        """
        # Log public key query start.
        start_log = logs.SSH_KEY_QUERY_START.format(ip=self.ip)
        self._logger.debug(start_log)
        try:
            key_dict = get_known_hosts()[self.ip]
        except KeyError:
            # IP address not found in the known hosts file.
            unknown_host_log = logs.SSH_KEY_QUERY_FAILURE.format(ip=self.ip)
            self._logger.info(unknown_host_log)
            pass
        else:
            # Log public key query success and return.
            key_name = key_dict.keys()[0]
            success_log = logs.SSH_KEY_QUERY_SUCCESS.format(
                key_name=key_name, ip=self.ip
            )
            self._logger.info(success_log)
            return key_dict[key_name]

    def create_transport(
        self, banner_timeout: int = None, socket_timeout: int = None
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
        # Log start
        start_log = logs.SSH_TRANSPORT_INIT_START.format(
            export_destination=self
        )
        self._logger.debug(start_log)
        # Create Transport instance.
        socket_timeout = (
            self.SOCKET_TIMEOUT if socket_timeout is None else socket_timeout
        )
        try:
            transport = paramiko.Transport(
                (self.ip, self.PORT), socket_timeout=socket_timeout
            )
        except Exception as e:
            # Log exception and re-raise,
            exception_log = logs.SSH_TRANSPORT_INIT_FAILURE.format(exception=e)
            self._logger.warn(exception_log)
            raise
        else:
            # Log success.
            success_log = logs.SSH_TRANSPORT_INIT_SUCCESS.format(
                export_destination=self
            )
            self._logger.info(success_log)
        # Increase banner timeout to prevent exception raised due to lack of
        # resources. See: https://stackoverflow.com/a/59453832/4416932.
        transport.banner_timeout = (
            self.BANNER_TIMEOUT if banner_timeout is None else banner_timeout
        )
        # Set encryption algorithm type.
        if self.key is not None:
            expected_name = self.key.get_name()
            transport._preferred_keys = [expected_name]
            # Log transport encryption key name.
            transport_key_log = logs.SSH_TRANSPORT_KEY.format(
                ip=self.ip, key_name=expected_name
            )
            self._logger.debug(transport_key_log)
        return transport

    def query_public_key(self) -> Tuple[str, bytes]:
        """
        Queries the remote host for a public key.

        Returns
        -------
        Tuple[str, bytes]
            Key type name, Value as bytes
        """
        # Log start.
        start_log = logs.SSH_HOST_KEY_QUERY_START.format(ip=self.ip)
        self._logger.debug(start_log)
        # Query host for public key.
        try:
            remote_key = self.transport.get_remote_server_key()
        except SSHException as e:
            # Log exception and re-raise.
            failure_log = logs.SSH_HOST_KEY_QUERY_FAILURE.format(
                ip=self.ip, exception=e
            )
            self._logger.info(failure_log)
            raise
        else:
            # Read key encryption name and value.
            name = remote_key.get_name()
            value = remote_key.asbytes()
            # Log success.
            success_log = logs.SSH_HOST_KEY_QUERY_SUCCESS.format(
                key_name=name, ip=self.ip
            )
            self._logger.info(success_log)
            return name, value

    def validate_public_key(self):
        """
        Validates the host's public key against the known hosts file.
        """
        if self.key:
            # Log validation start.
            start_log = logs.SSH_KEY_VALIDATION_START.format(ip=self.ip)
            self._logger.debug(start_log)
            # Read existing key information.
            expected_name = self.key.get_name()
            expected_value = self.key.asbytes()
            # Query key information from the host.
            name, value = self.query_public_key()
            # Check key validity.
            valid_key = name == expected_name and value == expected_value
            if not valid_key:
                # Log and raise exception for an invalid key.
                failure_log = logs.SSH_KEY_VALIDATION_FAILURE.format(
                    ip=self.ip, expected_name=expected_name, name=name
                )
                self._logger.warn(failure_log)
                raise SSHException(failure_log)
            # Log public key validation success.
            sucess_log = logs.SSH_KEY_VALIDATION_SUCCESS.format(ip=self.ip)
            self._logger.info(sucess_log)
        else:
            skip_log = logs.SSH_KEY_VALIDATION_SKIP.format(ip=self.ip)
            self._logger.info(skip_log)

    def authenticate(self):
        """
        Authenticate the transport session to the host using
        :attr:`username` and :attr:`password`.
        """
        # Log password authentication start.
        start_log = logs.SSH_PASSWORD_AUTH_START.format(
            export_destination=self
        )
        self._logger.debug(start_log)
        try:
            self.transport.auth_password(self.username, self.password)
        except Exception as e:
            failure_log = logs.SSH_TRANSPORT_INIT_FAILURE.format(
                export_destination=self, exception=e
            )
            self._logger.warn(failure_log)
        else:
            success_log = logs.SSH_PASSWORD_AUTH_SUCCESS.format(
                export_destination=self
            )
            self._logger.info(success_log)

    def connect(self, timeout: int = None) -> None:
        """
        Negotiates a connection with the host.

        Parameters
        ----------
        timeout : int
            SSH session negotiation timeout value (seconds)
        """
        if not self.transport.active:
            # Log SSH client session initialization start.
            start_log = logs.SSH_CONNECTION_START.format(
                export_destination=self
            )
            self._logger.debug(start_log)
            # Initialize SSH client session.
            timeout = self.SESSION_TIMEOUT if timeout is None else timeout
            try:
                self.transport.start_client(timeout=timeout)
            except SSHException as e:
                # Log raised exception and re-raise.
                failure_log = logs.SSH_CONNECTION_FAILURE.format(
                    export_destination=self, exception=e
                )
                self._logger.info(failure_log)
                raise
            else:
                # Log success.
                success_log = logs.SSH_CONNECTION_SUCCESS.format(
                    export_destination=self
                )
                self._logger.info(success_log)
            self.validate_public_key()
            self.authenticate()
        else:
            # Log existing active connection found.
            skip_log = logs.SSH_TRANSPORT_ACTIVE.format(
                export_destination=self
            )
            self._logger.debug(skip_log)

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
        # Log SFTP connection initialization.
        start_log = logs.SFTP_CLIENT_START.format(export_destination=self)
        self._logger.debug(start_log)
        # Establish SSH connection if it isn't already active.
        if not self.transport.active:
            self.connect()
        # Start SFTP client.
        try:
            sftp_client = paramiko.SFTPClient.from_transport(self.transport)
        except Exception as e:
            # Log exception and re-raise.
            failure_log = logs.SFTP_CLIENT_FAILURE.format(
                export_destination=self, exception=e
            )
            self._logger.warn(failure_log)
            raise
        else:
            # Log success and return SFTPClient instance.
            success_log = logs.SFTP_CLIENT_SUCCESS.format(
                export_destination=self
            )
            self._logger.info(success_log)
            # Disable relative path emulation, see:
            # https://docs.paramiko.org/en/stable/api/sftp.html#paramiko.sftp_client.SFTPClient.chdir
            sftp_client.chdir(path=None)
            return sftp_client

    def mkdir(
        self,
        path: Union[str, Path],
        parents: bool = True,
        exist_ok: bool = True,
    ):
        """
        Create directory within the host.

        Parameters
        ----------
        path : Union[str, Path]
            Directory path
        parents : bool
            Whether to create destination parents if they don't already exist
        exist_ok : bool
            Whether to raise an exception if the destination directory already
            exists
        """
        # Log directory creation start.
        start_log = logs.SFTP_MKDIR_START.format(
            path=path, export_destination=self
        )
        self._logger.debug(start_log)
        # Iterate given directory destination parts and try to create.
        directory_names = []
        for part in path.parts:
            if part == "/":
                continue
            # Create path instance for current iteration.
            directory_names.append(part)
            current_path = Path("/" + "/".join(directory_names))

            # If not *parents* and the current path is not the destination
            # path, skip to last iteration.
            if not (parents or part == path.name):
                continue
            # If *parents* and the current path is not the destination path,
            # try to create the parent.
            elif parents and part != path.name:
                self.mkdir(current_path, parents=False, exist_ok=exist_ok)
                continue
            # Handle destination directory creation.
            else:
                try:
                    # Check if the directory already exists.
                    self.sftp_client.stat(str(current_path))
                except FileNotFoundError:
                    # Directory does not exist, create it.
                    try:
                        self.sftp_client.mkdir(str(current_path))
                    except OSError as e:
                        # Log failure and re-raise.
                        failure_log = logs.SFTP_MKDIR_FAILURE.format(
                            export_destination=self,
                            path=current_path,
                            exception=e,
                        )
                        self._logger.warn(failure_log)
                        raise
                    else:
                        # Log success.
                        success_log = logs.SFTP_MKDIR_SUCCESS.format(
                            export_destination=self, path=current_path
                        )
                        self._logger.debug(success_log)
                else:
                    # Log existing directory found and raise or return.
                    log_exists = logs.SFTP_MKDIR_EXISTS.format(
                        path=current_path, export_destination=self
                    )
                    self._logger.debug(log_exists)
                    if not exist_ok:
                        raise OSError(log_exists)

    def _put(self, source: Path, destination: Path):
        """
        Utility method to reduce clutter due to logging and surrounding logic.

        Parameters
        ----------
        source : Path
            Local file to copy
        destination : Path
            Absolute destination in the host file system
        """
        # Create parent directory if needed.
        self.mkdir(destination.parent, parents=True, exist_ok=True)
        # Transfer file.
        try:
            self.sftp_client.put(str(source), str(destination), confirm=True)
        except OSError as e:
            # Log file transfer failure and re-raise.
            failure_log = logs.SFTP_PUT_FAILURE.format(
                source=source,
                export_destination=self,
                destination=destination,
                exception=e,
            )
            self._logger.warning(failure_log)
            raise
        else:
            # Log success and return.
            success_log = logs.SFTP_PUT_SUCCESS.format(
                source=source,
                export_destination=self,
                destination=destination,
            )
            self._logger.debug(success_log)

    def put(
        self,
        source: Union[Path, str, Iterable[Union[Path, str]]],
        destination: Union[Path, str] = None,
        exist_ok: bool = True,
        force: bool = False,
        progressbar: bool = False,
    ) -> None:
        """
        Copies *source* (a filesystem accessible file path) to *destination* in
        the host using SFTP.

        Parameters
        ----------
        source : Union[Path, str]
            Local file to copy
        destination : Union[Path, str]
            Destination in the host file system. if None, tries to use the
            *source* path relative to the application's MEDIA_ROOT
        exist_ok : bool, optional
            Whether to forgive trying to put an existing file (rather than
            raising an exception), default is True
        force : bool, optional
            Whether to override the file if it already exists in the host,
            default is False (if set to True, *exist_ok* is meaningless)
        progressbar : bool, optional
            Whether to display a progressbar or not, applicable only if
            *source* is an interable of paths, default is False
        """
        # Handle iterable of paths.
        if not isinstance(source, (Path, str)):
            try:
                # Create progressbar if *progressbar* is True.
                iterable = (
                    tqdm(source, unit="file", desc=f"Copying to {self}")
                    if progressbar
                    else source
                )
                # Iterate *source* and transfer files.
                for path in iterable:
                    self.put(path, destination, exist_ok=exist_ok, force=force)
            except TypeError:
                # If iteration failed, log and re-raise.
                bad_input_log = logs.SFTP_PUT_BAD_INPUT.format(
                    bad_type=type(source)
                )
                self._logger.warn(bad_input_log)
                raise
            else:
                return
        # Handle single file path.
        # Infer absolute destination path.
        destination = (
            Path(source).relative_to(settings.MEDIA_ROOT)
            if destination is None
            else destination
        )
        destination = (
            Path(destination)
            if Path(destination).is_absolute()
            else Path(self.destination) / destination
        )
        # Log file transfer start.
        start_log = logs.SFTP_PUT_START.format(
            source=source, export_destination=self, destination=destination
        )
        self._logger.debug(start_log)
        # Look for an existing file at the destination.
        try:
            self.sftp_client.stat(str(destination))
        except FileNotFoundError:
            # No existing file found, continue to file transfer.
            pass
        else:
            # Log existing file found.
            exists_log = logs.SFTP_PUT_EXISTS.format(
                export_destination=self, destination=destination
            )
            self._logger.debug(exists_log)
            # Handle existing file found and *force* is False.
            if not force:
                # Log transfer termination and return.
                abort_log = logs.SFTP_PUT_ABORT.format(
                    source=source,
                    export_destination=self,
                    destination=destination,
                )
                self._logger.debug(abort_log)
                return
            # Handle existing file found and *exist_ok* is False.
            elif not exist_ok:
                raise OSError(exists_log)
        # Create parent directory if needed.
        self.mkdir(destination.parent, parents=True, exist_ok=True)
        # Transfer file.
        self._put(source, destination)

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
