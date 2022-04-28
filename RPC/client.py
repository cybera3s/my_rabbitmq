import pika
import uuid


class Sender:
    def __init__(self):
        """
        initialize connection, channel and declare a nameless queue and assign it to self.queue
        and at last basic consume on that queue bu auto acknowledgement and self.on_response method as callback
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.ch = self.connection.channel()
        result = self.ch.queue_declare(queue='', exclusive=True)
        self.qname = result.method.queue
        self.ch.basic_consume(queue=self.qname, on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, prop, body):
        """
        used as call callback on messages deliver and check if correlation code of instance equal to
        delivered message correlation id then assign self.response to message body
        :param ch: message channel
        :param method: message meta data
        :param prop: message properties
        :param body: message text body
        :return: no return just assign
        """
        if self.corr_id == prop.correlation_id:
            self.response = body

    def call(self, n: int):
        """
        set response to none
        create instance correlation id bu using uuid module
        publish with empty exchange (default=direct) and a named routing key with properties reply to assigned to queue
        name that initialized in init method and pass already created correlation id and pass n as a string for body
        and then wait for response from server by while loop
        at last return the self.response
        :param n: parameter as call method for doing some procedure on server
        :return: self.response
        """
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.ch.basic_publish(exchange='', routing_key='rpc_queue',
                              properties=pika.BasicProperties(reply_to=self.qname, correlation_id=self.corr_id),
                              body=str(n))
        print('Server is Processing...')

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)


send = Sender()
resp = send.call(int(input('Enter your Number: ')))
print(f'Response is {resp}')
