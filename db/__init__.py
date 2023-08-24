from redis import Redis

class Database:
    redis_client = None

    @classmethod
    def initial(self):
        self.redis_client = Redis(host='localhost', port=6379, db=2)

    @classmethod
    def insert(self, name, key, value):
        self.redis_client.hsetnx(name, key, value)

    @classmethod
    def length(self, name):
        return self.redis_client.hlen(name)