import os
import socket

from datetime import datetime
from django.db import models
from django.urls import reverse
from research.models.data_source import DataSource
from smb.SMBConnection import SMBConnection
from .smb_file import SMBFile


class SMBDirectory(DataSource):
    user_id = models.CharField(max_length=64, blank=False)
    password = models.CharField(max_length=64, blank=False)
    share_name = models.CharField(max_length=64, blank=False)
    server_name = models.CharField(max_length=64, blank=False)
    last_sync = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "SMB Directories"

    def get_absolute_url(self):
        return reverse('smb_directory_list')

    def get_server_ip(self) -> str:
        return socket.getaddrinfo(self.server_name, 139)[0][-1][0]

    def get_client_name(self) -> str:
        return socket.gethostname()

    def create_connection(self) -> SMBConnection:
        return SMBConnection(
            self.user_id,
            self.password,
            self.get_client_name(),
            self.server_name,
        )

    def connect(self) -> SMBConnection:
        conn = self.create_connection()
        ip_address = self.get_server_ip()
        # This function is called also when checking whether the directory
        # is accessible, so the timeout prevents long loading times.
        try:
            if conn.connect(ip_address, timeout=1):
                return conn
            return False
        # In case no route is found to the host
        except OSError:
            return False

    def list_files(self, location: str):
        connection = self.connect()
        files = connection.listPath(self.share_name, location)
        connection.close()
        result = []
        for path in files[2:]:
            full_path = os.path.join(location, path.filename)
            if path.isDirectory:
                result += self.list_files(full_path)
            else:
                result += [full_path]
        return result

    def list_all_files(self):
        return self.list_files('.')

    def sync(self):
        files = self.list_all_files()
        for f in files:
            found = self.file_set.filter(path=f).first()
            if not found:
                new_file = SMBFile(
                    path=f,
                    source=self,
                )
                new_file.save()
        self.last_sync = datetime.now()
        self.save()

    @property
    def is_connected(self):
        connection = self.connect()
        if connection:
            connection.close()
            return True
        return False

    def __str__(self):
        return self.name
