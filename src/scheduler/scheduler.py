#!/usr/bin/env python
import pika
import json
import schedule
from threading import Thread, Event
import time
from json import JSONDecodeError
import redis
from src.scheduler.rpc_server import RpcServer

"""
{
    "email": "anlcnydn@gmail.com",
    "subscriptions": ["anlcnydn", "alirizakeles"],
    "period": "weekly" // daily, weekly
}
"""

# Blocking connection calismazsa SelectConnection'a cevrilmeli
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))


class Scheduler(RpcServer):
    def __init__(self):
        self.QUEUE = 'ab18-.rpc_queue'
        self.EXCHANGE = 'ab18-.exchange'
        self.VIRTUAL_HOST = 'ab18'
        self.CREDENTIALS = pika.PlainCredentials('ab18', '1')
        self._closing = False
        super(RpcServer, self).__init__()

    def on_request(self, ch, method, props, body):
        """
        https://www.rabbitmq.com/tutorials/tutorial-six-python.html
        """

        err = None

        try:
            body = json.loads(body)
            params = body.get('params')

            self.schedule_the_job(params.get('period'), params.get('email'))
            self.save_to_db(params)

        except JSONDecodeError as e:
            err_msg = "Body cannot be decoded. It may not be a valid " \
                      "json. Message: {}".format(e)
            err = {"code": -32700, "message": err_msg}
        except Exception as e:
            err_msg = "Internal Error: {}".format(e)
            err = {"code": -32700, "message": err_msg}

        response = {
            "jsonrpc": "2.0",
            "id": id
        }

        if err:
            response['error'] = err
        else:
            response['result'] = params
            response['result']['status'] = "success"

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        """
        Overrided this method to use on_request callback
        Original method in rpc_server.py

        """
        self.add_on_cancel_callback()
        self._channel.basic_qos(prefetch_count=1)
        self._consumer_tag = self._channel.basic_consume(
            consumer_callback=self.on_request,
            queue=self.QUEUE
        )
        print("Started consuming...")

    def save_to_db(self, params):
        # todo implement
        pass

    def notify_crawler(self, subscriber=None):
        if subscriber:
            # todo notify the crawler about it is the time for subscriber
            pass

    def schedule_the_job(self, period, subscriber):
        job_without_interval = schedule.every()

        if period == 'daily':
            job_with_an_interval = job_without_interval.day()
        else:
            job_with_an_interval = job_without_interval.week()

        return job_with_an_interval.do(self.notify_crawler, subscriber=subscriber)

    def run_continuously(self, interval=1):
        """
        https://raw.githubusercontent.com/mrhwick/schedule/master/schedule/__init__.py
        """
        print("Started to run continuously")
        cease_continuous_run = Event()

        class ScheduleThread(Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run


def main():
    scheduler = Scheduler()
    t1 = Thread(target=scheduler.run)
    t2 = Thread(target=scheduler.run_continuously)
    t1.start()
    t2.start()
    print("Started RpcServer...")


if __name__ == '__main__':
    main()




