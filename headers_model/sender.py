from pika import BlockingConnection, ConnectionParameters, BasicProperties

connection = BlockingConnection(ConnectionParameters(host='localhost'))

with connection as conn:
    channel = conn.channel()
    channel.exchange_declare(exchange='headers', exchange_type='headers')

    channel.basic_publish(exchange='headers', routing_key='', body='Test Headers',
                          properties=BasicProperties(headers={'level': 'info'}))
    print('Message Sent!')