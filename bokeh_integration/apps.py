from django.apps import AppConfig
from bokeh.server.server import Server
from bokeh.application import Application
import asyncio

from bokeh_integration import app


class BokehConfig(AppConfig):
    name = "bokeh"

    def ready(self):
        self.start_bokeh_server()

    def start_bokeh_server(self):
        print("MERD")
        server = Server(
            {"/bokeh": Application(app)},
            io_loop=asyncio.new_event_loop(),
            port=4343,
            # bokeh_applications,  # list of Bokeh applications
            # io_loop=loop,        # Tornado IOLoop
            # **server_kwargs      # port, num_procs, etc.
        )

        # start timers and services and immediately return
        server.start()
        server.io_loop.start()
