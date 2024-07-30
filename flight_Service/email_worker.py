import os
import django
from django.core.mail import send_mail
from django.conf import settings



import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrackYourFlight_App.settings')
django.setup()

from auth_Service.controllers import AuthController
from config import Config


RABBITMQ_CONN = Config.RABBITMQ_CONN


def send_email_notification(flight):
    users = AuthController().get_users_subscribed_to_notified(flight['airline'],flight['flight_number'])
    for user in users:
        send_mail(
            subject='Flight Status Update',
            message=flight['msg'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

def callback(ch, method, properties, body):
    flight = json.loads(body)
    send_email_notification(flight)


def start_consumer():

    RABBITMQ_CONN.basic_consume(queue='flight_notifications',
                                on_message_callback=callback,
                                auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    RABBITMQ_CONN.start_consuming()

if __name__ == '__main__':
    start_consumer()