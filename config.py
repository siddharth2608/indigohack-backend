from ConnectionUtils.dbconnections import PostgresConnection
import redis
import pika

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


    def create_rabbitmq_connection():
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='flight_notifications')
        return channel


    RABBITMQ_CONN = create_rabbitmq_connection()

    MAIL_CONFIG = {
        'gmail_user':'example@gmail.com',
        'gmail_password' : 'app_password'
    }