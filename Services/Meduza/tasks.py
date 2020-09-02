from Core.tasks import Task


class Parser(Task):
    kind = 'Meduza.Parser'
    routing_key = 'meduza_routing_key'


class Scanner(Task):
    kind = 'Meduza.Scanner'
    routing_key = 'meduza_routing_key'
