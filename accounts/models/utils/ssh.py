"""
Utility functions for SSH functionality.
"""
import os

import paramiko
from django.conf import settings

#
# Django settings keys.
#
#: Setting key for the RSA key file path on the server.
# RSA_KEY_SETTING: str = "SSH_RSA_KEY"
#: Setting key for the known hosts file path on the server.
KNOWN_HOSTS_SETTINGS: str = "SSH_KNOWN_HOSTS"

#
# Default SSH settings.
#
#: Default RSA key file path.
# DEFAULT_RSA_KEY_PATH = os.path.expanduser("~/.ssh/id_rsa")
#: Default known hosts file path.
DEFAULT_KNOWN_HOSTS_PATH = os.path.expanduser("~/.ssh/known_hosts")


# def get_rsa_key() -> paramiko.rsakey.RSAKey:
#     """
#     Returns the server's RSA key.

#     Returns
#     -------
#     paramiko.rsakey.RSAKey
#         Server RSA key
#     """
#     rsa_path = getattr(settings, RSA_KEY_SETTING, DEFAULT_RSA_KEY_PATH)
#     return paramiko.RSAKey.from_private_key_file(rsa_path)


def get_known_hosts() -> paramiko.hostkeys.HostKeys:
    """
    Returns the server's known hosts configuration.

    Returns
    -------
    paramiko.hostkeys.HostKeys
        Known host keys
    """
    known_hosts_path = getattr(
        settings, KNOWN_HOSTS_SETTINGS, DEFAULT_KNOWN_HOSTS_PATH
    )
    return paramiko.util.load_host_keys(known_hosts_path)
