import signal

from functools import partial
from utils import handle_interrupt, start_servers, wait_forever


if __name__ == "__main__":
    processes = start_servers()
    handler = partial(handle_interrupt, processes=processes)
    signal.signal(signal.SIGINT, handler)
    wait_forever()
