from queue import Queue
from pymyorm.singleton import Singleton
from pymyorm.connection import Connection


@Singleton
class ConnectionPool(object):

    def __init__(self):
        self.__size = 0
        self.__pool = None
        self.__debug = False
        self.__ping = 3600

    def create(self, host, port, user, password, database, charset='utf8', debug=False):
        if self.__pool is not None:
            del self.__pool

        if self.__size <= 0:
            raise Exception('connection pool size error')

        self.__debug = debug

        self.__pool = Queue(self.__size)
        for _ in range(0, self.__size):
            conn = Connection(host=host, port=port, user=user, password=password, database=database, charset=charset)
            conn.open(self.__debug)
            conn.set_ping(self.__ping)
            self.put(conn)

    def put(self, conn):
        try:
            if self.__debug:
                print('put connection into pool')
            self.__pool.put(conn)
        except Exception as e:
            if self.__debug:
                print('put connection into pool error')
            raise e

    def get(self):
        try:
            if self.__debug:
                print('get connection from pool')
            conn = self.__pool.get()
            conn.ping()
            return conn
        except Exception as e:
            if self.__debug:
                print('get connection from pool error')
            raise e

    def size(self, size):
        self.__size = size

    def ping(self, seconds):
        self.__ping = seconds
