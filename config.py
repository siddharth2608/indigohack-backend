from ConnectionUtils.dbconnections import PostgresConnection

class Config:

    POSTGRES_CONFIG = {
        'host': '127.0.0.1',
        'user': 'siddharth',
        'password': 'root@123',
        'dbname': 'flight_tracker',
        'port': 5432
    }

    POSTGRESSQL_CONN = PostgresConnection(POSTGRES_CONFIG)