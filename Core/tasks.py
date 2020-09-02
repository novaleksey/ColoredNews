import json


class Task:
    exchange = 'Tasks'
    routing_key = ''

    kind = NotImplemented
    params = None

    @classmethod
    def create_task(cls, rabbit_channel, msg=None):
        rabbit_channel.basic_publish(
            exchange=cls.exchange,
            routing_key=cls.routing_key,
            body=cls._prepare_msg_body(msg)
        )

    @classmethod
    def _prepare_msg_body(cls, msg):
        return json.dumps({
            'kind': cls.kind,
            'params': cls.params,
            'message': msg
        })
