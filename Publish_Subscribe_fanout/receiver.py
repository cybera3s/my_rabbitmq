from pika import BlockingConnection, ConnectionParameters

connection = BlockingConnection(ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue = result.method.queue

channel.queue_bind(queue=queue, exchange='logs')

print('waiting for logs exit ctrl+c')


def callback(ch, method, properties, body):
    print(f'log: {body}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue, on_message_callback=callback)
channel.start_consuming()
