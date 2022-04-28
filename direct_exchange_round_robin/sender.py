"""
basic sender with named queue declaration and direct exchange
and round robin dispatching
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch1 = connection.channel()
ch1.queue_declare(queue='hello')

ch1.basic_publish(exchange='', routing_key='hello', body='Hi There',
                  properties=pika.BasicProperties(headers={'name': 'Ario'}, content_type='application/json'))
print('message sent')
connection.close()
