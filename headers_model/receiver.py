from pika import BlockingConnection, ConnectionParameters, BasicProperties

connection = BlockingConnection(ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='headers', exchange_type='headers')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

level = input('Enter level : ')
hardness = int(input('Enter Hardness: '))

channel.queue_bind(queue=queue_name, exchange='headers',
                   arguments={'x-match': 'any', 'level': level, 'hardness': hardness})


def callback(ch, method, prop, body):
    print(f'Received {body}')


print('Waiting for messages...')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
