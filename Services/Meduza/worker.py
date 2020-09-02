from datetime import timedelta

from . import tasks
from . import handlers


class MeduzaConsumer:
    queue = 'Meduza'
    routing_key = 'meduza_routing_key'
    handler = handlers.MeduzaHandler()

    routing = {
        tasks.Scanner.kind: handler.handle_scanner,
        tasks.Parser.kind: handler.handle_parser
    }


class MeduzaProducer:

    # Период сканирования источника
    scanner_timeout = timedelta(hours=1)
    exchange = 'Tasks'
    consumer = MeduzaConsumer
    publishers = (
        tasks.Scanner,
        # tasks.Parser
    )

