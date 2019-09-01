from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from socketio.sdjango import namespace


_connections = {}


@namespace("/kitchen")
class KitchenNamespace(BaseNamespace, BroadcastMixin):
    def initialize(self, *args, **kwargs):
        _connections[id(self)] = self
        super(KitchenNamespace, self).initialize(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        del _connections[id(self)]
        super(KitchenNamespace, self).disconnect(*args, **kwargs)

    def recv_disconnect(self):
        self.disconnect(silent=True)
        return True
