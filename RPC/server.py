from pika import BlockingConnection, ConnectionParameters, BasicProperties
import time

connection = BlockingConnection(ConnectionParameters(host='localhost'))

ch = connection.channel()
# declare queue with the same name as routing key in call method client
ch.queue_declare(queue='rpc_queue')


def callback(channel, method, prop, body):
    """
    do some procedure on message then publish it for client with empty exchange and
    routing_key assigned to message properties reply_to along with properties such as
    correlation_id assigned to message properties correlation_id (same as client correlation_id)
    and body of procedure response
    at last send acknowledgement to queue
    :param channel: message channel
    :param method: message meta data
    :param prop: message properties
    :param body: message body
    """
    n = int(body)
    print('Processing message...')
    time.sleep(4)
    response = n + 1
    channel.basic_publish(exchange='', routing_key=prop.reply_to,
                          properties=BasicProperties(correlation_id=prop.correlation_id), body=str(response))
    channel.basic_ack(delivery_tag=method.delivery_tag)


# limit number of messages for workers
ch.basic_qos(prefetch_count=1)
# consume on mentioned queue
ch.basic_consume(queue='rpc_queue', on_message_callback=callback)
print('waiting for message...')
ch.start_consuming()
