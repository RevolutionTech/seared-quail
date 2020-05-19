from os import environ, getpid, kill
from re import match
from signal import SIGINT
from threading import Thread
from time import sleep

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import naiveip_re
from django.utils.autoreload import code_changed, restart_with_reloader
from socketio.server import SocketIOServer

RELOAD = False


def reload_watcher():
    global RELOAD
    while True:
        RELOAD = code_changed()
        if RELOAD:
            kill(getpid(), SIGINT)
        sleep(1)


class Command(BaseCommand):
    def add_arguments(self, parser):
        try:
            default_port = settings.SOCKETIO_PORT
        except AttributeError:
            default_port = "8000"

        parser.add_argument(
            "addrport",
            nargs="?",
            default=f"0.0.0.0:{default_port}",
            help="Specify the address and port used by the SocketIOServer",
        )

    def handle(self, *args, **options):
        addrport = options["addrport"]
        m = match(naiveip_re, addrport)
        if m is None:
            raise CommandError(
                "%s is not a valid port number or address:port pair." % addrport
            )

        self.addr, _, _, _, self.port = m.groups()

        # Make the port available allowing the port
        # to be set as the client-side default
        environ["DJANGO_SOCKETIO_PORT"] = str(self.port)

        Thread(target=reload_watcher).start()
        try:
            print(
                "\nSocketIOServer running on {addr}:{port}\n".format(
                    addr=self.addr, port=self.port
                )
            )
            handler = self.get_handler(*args, **options)
            bind = (self.addr, int(self.port))
            server = SocketIOServer(
                bind, handler, resource="socket.io", policy_server=True
            )
            server.serve_forever()
        except KeyboardInterrupt:
            if RELOAD:
                server.stop()
                print("Reloading...")
                restart_with_reloader()
            else:
                raise

    def get_handler(self, *args, **options):
        """
        Returns the django.contrib.staticfiles handler
        """
        handler = WSGIHandler()
        try:
            from django.contrib.staticfiles.handlers import StaticFilesHandler
        except ImportError:
            return handler
        use_static_handler = options.get("use_static_handler", True)
        insecure_serving = options.get("insecure_serving", False)
        if (
            settings.DEBUG
            and use_static_handler
            or (use_static_handler and insecure_serving)
        ):
            handler = StaticFilesHandler(handler)
        return handler
