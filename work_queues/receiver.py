"""
#direct_exchange_round_robin: create connection and set host/ip and port
#work_queues: create channel
#3: declaring queue and durability
#4: callback function to do a task after getting message
#5: set manual acknowledgement of message to be sure that task is fully done
#6: set quality of service to split tasks one at a time to a free consumer
#7: declare consuming method and call back task
#8: start loop of consuming
"""

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))   # direct_exchange_round_robin
ch = connection.channel()   # work_queues

ch.queue_declare(queue='first', durable=True)   # 3
print('Waiting for message, press ctrl+c to exit')


def callback(ch, method, properties, body):     # 4
    print(f"Received Body: {body}")
    # print(properties.headers)
    # print(f"Id of message: {method.delivery_tag}")
    # print(method)
    time.sleep(5)
    print('Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)      # 5


ch.basic_qos(prefetch_count=1)      # 6
ch.basic_consume(queue='first', on_message_callback=callback)   # 7
ch.start_consuming()        # 8
