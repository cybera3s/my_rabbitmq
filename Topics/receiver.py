from pika import BlockingConnection, ConnectionParameters

connection = BlockingConnection(ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare('topic_exchange', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

key = input('Enter Pattern: ')
# bind the declared queue and named exchange along with routing_key(binding _key) set to entered pattern
channel.queue_bind(queue=queue_name, exchange='topic_exchange', routing_key=key)


def callback(ch, method, properties, body):
    print(f"Received : {body} with {method.routing_key}")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print('waiting for log message: ')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print('\nStopped')
