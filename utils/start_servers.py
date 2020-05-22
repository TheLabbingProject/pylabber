import socket
import subprocess


PORTS = {"bokeh": 5006, "django": 8000, "vue": 8080}
COMMANDS = {
    "bokeh": [
        "bokeh",
        "serve",
        "--allow-websocket-origin",
        f"127.0.0.1:{PORTS['django']}",
        "--allow-websocket-origin",
        f"localhost:{PORTS['django']}",
        "--allow-websocket-origin",
        f"127.0.0.1:{PORTS['vue']}",
        "--allow-websocket-origin",
        f"localhost:{PORTS['vue']}",
        "--websocket-max-message-size",
        "10000",
        "plots/series/series_viewer",
    ],
    "django": ["./manage.py", "runserver"],
    "vue": ["npm", "run", "--prefix", "../vuelabber", "serve"],
}


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def start_server(service_name: str) -> subprocess.Popen:
    port = PORTS[service_name]
    if not is_port_in_use(port):
        command = COMMANDS[service_name]
        return subprocess.Popen(command)


def start_servers() -> dict:
    return {service_name: start_server(service_name) for service_name in COMMANDS}
