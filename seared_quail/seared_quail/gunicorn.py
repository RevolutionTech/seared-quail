bind = '0.0.0.0:8001'
max_requests = 10000
worker_class = 'socketio.sgunicorn.GeventSocketIOWorker'
workers = 1


def post_fork(server, worker):
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()
