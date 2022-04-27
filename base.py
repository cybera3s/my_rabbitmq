from pika import ConnectionParameters, BlockingConnection


class Initial:
    HOST = 'localhost'
    PORT = 5672

    def __init__(self, host: str = HOST, port: int = PORT):
        self.connection = BlockingConnection(ConnectionParameters(host=host, port=port))
        self._channel = self.connection.channel()

    @property
    def get_channel(self):
        return self._channel


class Publisher(Initial):
    exchange_name = None
    queue_name = None

    def declare_queue(self, queue_name: str, **kwargs):
        self.queue_name = queue_name
        return self.get_channel.queue_declare(queue=queue_name, **kwargs)

    def declare_exchange(self, exchange_name, ex_type=None, **kwargs):
        self.get_channel.exchange_declare(exchange=exchange_name, exchange_type=ex_type, **kwargs)
        self.exchange_name = exchange_name

    def _get_exchange(self):
        if self.exchange_name:
            return self.exchange_name
        return NameError('Exchange Name is not declared!')

    def _get_queue(self):
        if self.queue_name:
            return self.queue_name
        return NameError('Queue Name is not declared!')

    def publishing(self, exchange_name, routing_key, message_body):
        self.get_channel.basic_publish(exchange=self._get_exchange() if self.exchange_name else exchange_name,
                                       routing_key=routing_key, body=message_body)
        self.close()

    def close(self):
        self.connection.close()


p1 = Publisher()
p1.declare_exchange('test')
print(p1.get_channel)
