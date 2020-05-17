import threading


def wait_forever() -> None:
    forever = threading.Event()
    forever.wait()
