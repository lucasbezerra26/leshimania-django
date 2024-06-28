from psycogreen.gevent import patch_psycopg


def post_fork(_, worker):
    patch_psycopg()
    worker.log.info("Made Psycopg2 Green")


worker_class = "gevent"
workers = 1
worker_connections = 1000

timeout = 45
graceful_timeout = 45
