import time
import json
import asyncio
import logging
from threading import Thread
from importlib import import_module
from datetime import datetime

import pika

from Models.settings import Settings
from Models.base import DBSession
from Services.workers import service_producers, services_path


_EXCHANGE = 'Tasks'


class WorkerThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db_session = DBSession()
        # TODO в переменные окружения
        self.exchange = _EXCHANGE
        self.rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        log_format = "%(asctime)s: %(message)s"
        logging.basicConfig(
            format=log_format,
            level=logging.INFO,
            datefmt="%H:%M:%S"
        )


class Consumer(WorkerThread):

    def __init__(self, producers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        producers_list = producers
        self.consumers = [producer.consumer for producer in producers_list]

        self._rabbit_consume_channel = self.rabbit_connection.channel()
        self.routing = {}
        self._init_queues()
        self.build_routing()

    def run(self) -> None:
        while True:
            self.pull_actual_requests()

    def do_request_route(self, channel, method, properties, body):
        body_dict = json.loads(body)
        handle_func = self.routing.get(body_dict.get('kind'))
        if handle_func:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(handle_func(body_dict, channel))
            logging.info(f'New request {body_dict}')
            time.sleep(1)
        else:
            raise Exception(f'Нет обработчика для задачи {body_dict.get("kind")}')

    def _init_queues(self):
        for consumer in self.consumers:
            queue = consumer.queue
            self._rabbit_consume_channel.queue_declare(
                queue=queue,
                durable=True,
                exclusive=True
            )
            self._rabbit_consume_channel.queue_bind(
                queue=queue,
                exchange=self.exchange,
                routing_key=consumer.routing_key
            )
            self._rabbit_consume_channel.basic_consume(
                queue=queue,
                on_message_callback=self.do_request_route,
                auto_ack=True
            )

    def build_routing(self):
        for consumer in self.consumers:
            self.routing.update(consumer.routing)

    def pull_actual_requests(self):
        self._rabbit_consume_channel.start_consuming()
        time.sleep(1)


class Producer(WorkerThread):

    _DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rabbit_publish_channel = self.rabbit_connection.channel()

        self._rabbit_publish_channel.exchange_declare(
            exchange=self.exchange,
            durable=True
        )

        self._producers = self.collect_producers()

        self.child_factory = Consumer(producers=self._producers)
        self.child_factory.start()

    def run(self) -> None:
        while True:
            for producer in self._producers:
                self.check_for_new_job(producer.publishers, producer.scanner_timeout)
            # time.sleep(1)

    @staticmethod
    def collect_producers():
        producers = []
        for module_name, cls_name in service_producers:
            module = import_module(f'{services_path}.{module_name}')
            producer_cls = getattr(module, cls_name)
            producers.append(producer_cls)
        return producers

    def check_for_new_job(self, tasks, timeout):
        for task in tasks:
            rows = self._db_session.query(Settings).filter(Settings.setting_key == task.kind).all()
            need_new_point = False
            new_point = None
            if rows:
                last_run = datetime.strptime(rows[0].setting_value, self._DATETIME_FORMAT)
                if datetime.now() - last_run > timeout:
                    need_new_point = True
                    rows[0].setting_value = datetime.strftime(datetime.now(), self._DATETIME_FORMAT)
                    new_point = rows[0]
            else:
                need_new_point = True
                new_point = Settings(task.kind, datetime.strftime(datetime.now(), self._DATETIME_FORMAT))

            if need_new_point:
                logging.info('New Task created')
                task.create_task(self._rabbit_publish_channel)
                self._db_session.add(new_point)
                self._db_session.commit()
