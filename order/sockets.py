from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace

_connections = {}


@namespace("/kitchen")
class KitchenNamespace(BaseNamespace, BroadcastMixin):
    def initialize(self, *args, **kwargs):
        _connections[id(self)] = self
        super().initialize(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        del _connections[id(self)]
        super().disconnect(*args, **kwargs)

    def recv_disconnect(self):
        self.disconnect(silent=True)
        return True
