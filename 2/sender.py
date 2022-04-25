import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch1 = connection.channel()

ch1.queue_declare(queue='first', durable=True)
message = 'Testing message'

ch1.basic_publish(exchange='', routing_key='first', body=message,
                  properties=pika.BasicProperties(delivery_mode=2))

print('message sent')
connection.close()