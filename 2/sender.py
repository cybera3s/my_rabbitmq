"""
#1: create connection and declare host/ip port
#2: create channel
#3: declare queue and durability
#4: define publish method and body of message with some extra properties
#5: close connection
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))  # 1
ch1 = connection.channel()  # 2

ch1.queue_declare(queue='first', durable=True)  # 3
message = 'Testing message'

ch1.basic_publish(exchange='', routing_key='first', body=message,
                  properties=pika.BasicProperties(delivery_mode=2,
                                                  headers={'name': 'ario'}))  # ->  expiration='2000'   # 4

print('message sent')
connection.close()  # 5
