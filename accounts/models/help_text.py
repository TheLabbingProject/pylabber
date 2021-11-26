"""
Help text strings for the :mod:`~accounts.models` module.
"""

SSH_PORT: str = "Port used for SSH2 transport session initialization"
SSH_BANNER_TIMEOUT: str = "Timeout for an SSH banner to be presented (seconds)"
SSH_SOCKET_TIMEOUT: str = "Timeout for socket creation (seconds)"
SSH_NEGOTIATION_TIMEOUT: str = "Timeout for SSH2 session negotiation (seconds)"
EXPORT_DESTINATION_IP: str = "SSH server host IP address"
EXPORT_DESTINATION_USERNAME: str = "Username used for SSH authentication"
EXPORT_DESTINATION_PASSWORD: str = "Password used for SSH authentication"
EXPORT_DESTINATION_USERS: str = "Users that will have access to this export destination."
EXPORT_DESTINATION_PATH: str = "Base path on the host to use for relative file transfers"

# flake8: noqa: E501
