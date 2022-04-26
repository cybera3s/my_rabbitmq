import random

from pika import BlockingConnection, ConnectionParameters

connection = BlockingConnection(ConnectionParameters(host='localhost'))
with connection as conn:
    channel = conn.channel()
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    severity = ['info', 'warning', 'error']
    msg = random.choice(severity)
    channel.basic_publish(exchange='direct_logs', routing_key=msg, body=f'log {msg}')
    print(f'{msg} Message Sent!')

