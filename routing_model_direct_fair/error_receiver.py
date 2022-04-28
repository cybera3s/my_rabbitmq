from pika import BlockingConnection, ConnectionParameters

connection = BlockingConnection(ConnectionParameters(host='localhost'))
ch = connection.channel()
ch.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = ch.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

ch.queue_bind(queue=queue_name, exchange='direct_logs', routing_key='error')


def callback(ch, method, properties, body):
    with open('logs.log', 'a') as f:
        print(body, file=f)
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue=queue_name, on_message_callback=callback)

print('Waiting for Error messages')
ch.start_consuming()
