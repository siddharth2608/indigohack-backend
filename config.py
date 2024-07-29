from ConnectionUtils.dbconnections import PostgresConnection
import redis

class Config:

    POSTGRES_CONFIG = {
        'host': '127.0.0.1',
        'user': 'siddharth',
        'password': 'root@123',
        'dbname': 'flight_tracker',
        'port': 5432
    }

    POSTGRESSQL_CONN = PostgresConnection(POSTGRES_CONFIG)
    REDIS_CONN = redis.StrictRedis(host='localhost', port=6379, db=0)