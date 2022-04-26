import random
import pika
from pika import ConnectionParameters

connection = pika.BlockingConnection(ConnectionParameters(host='localhost'))
ch1 = connection.channel()
# define exchange and its type
ch1.exchange_declare(exchange='logs', exchange_type='fanout')

message = ['debug', 'info', 'warning', 'error', 'critical']
ch1.basic_publish(exchange='logs', routing_key='', body=random.choice(message))

print('Message Sent !')
connection.close()
