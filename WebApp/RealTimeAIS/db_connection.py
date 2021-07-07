import psycopg2 as pg
from sshtunnel import SSHTunnelForwarder
from . import SECRET

server = None


def get_postgres():
    return pg.connect(
        dbname='collected_ais',
        user='ais_app_user',
        port="5431",
        password='apPW4197@nxzt')


def open_tunnel():
    server = SSHTunnelForwarder(
        'bigdata2.research.cs.dal.ca',
        ssh_username=SECRET.USERNAME,
        ssh_password=SECRET.PASSWORD,
        remote_bind_address=('127.0.0.1', 3000)
    )

    server.start()


def close_tunnel():
    server.stop()
