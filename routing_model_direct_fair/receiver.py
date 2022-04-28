from pika import BlockingConnection, ConnectionParameters

connection = BlockingConnection(ConnectionParameters())
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# declare nameless queue and let it be random and exclusive
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = ['info', 'warning']

# bind queue and exchanges for each item in severities
for severity in severities:
    channel.queue_bind(queue=queue_name, exchange='direct_logs', routing_key=severity)      # routing_key -> binding key


def callback(ch, method, properties, body):
    print(f"Received : {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


print(f'Waiting for {" & ".join(severities)} logs...')
channel.basic_consume(queue=queue_name, on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print('Consuming Stopped!')


