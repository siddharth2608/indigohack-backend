import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django
from django.conf import settings
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TrackYourFlight_App.settings')
django.setup()

from auth_Service.controllers import AuthController
from config import Config


RABBITMQ_CONN = Config.RABBITMQ_CONN

def send_mail(email,body):

	gmail_user = 'siddharthsrivastav987@gmail.com'
	gmail_password = 'exnlnujdcwjetcpm'

	sent_from = 'TrackYourFlight'
	to = [email]
	subject = 'Flight Status Update'
	
	msg = MIMEMultipart()
	msg['From'] = sent_from
	msg['To'] = ", ".join(to)
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP_SSL("smtp.gmail.com",465)
	server.ehlo()
	server.starttls
	server.login(gmail_user, gmail_password)
	server.sendmail(sent_from, to, msg.as_string())
	server.quit()

	print('Email sent!')

def send_email_notification(flight):
	users = AuthController().get_users_subscribed_to_notified(flight['airline'],flight['flight_number'])
	print(users)
	for user in users:
		send_mail(user['email'],flight['msg'])

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