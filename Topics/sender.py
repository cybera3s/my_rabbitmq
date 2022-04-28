from pika import BlockingConnection, ConnectionParameters

connection = BlockingConnection(ConnectionParameters(host='localhost'))
channel = connection.channel()

with connection as conn:
    channel.exchange_declare('topic_exchange', exchange_type='topic')  # set exchange as topic
    message = 'log message'
    key = input('Enter pattern: ')
    channel.basic_publish(exchange='topic_exchange', routing_key=key, body=message)
    print('Message Sent!')