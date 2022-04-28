"""
basic receiver with named queue and direct exchange
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch2 = connection.channel()

ch2.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(f"Received  {body}")
    print(f"properties {properties}")
    print(f'Channel {ch}')
    print(f'method {method}')


# auto acknowledgement removes message from queue
ch2.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print('waiting for message, exit ctrl+c')
# connection.process_data_events()
ch2.start_consuming()
