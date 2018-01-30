import json
import redis
import pika
import schedule
import time
import threading

r = redis.Redis()
p = pika.BlockingConnection(pika.ConnectionParameters(host='10.21.251.26', virtual_host='ab18-vhost', credentials=pika.PlainCredentials('ab18-user', 'microservices')))
sub_ch = p.channel()
sub_ch.exchange_declare(exchange='work', exchange_type='direct')
rest_ch = p.channel()
rest_ch.queue_declare(queue='scheduler_queue')

periods = {"daily" : 1, "weekly" : 7, "monthly" : 30}
funcs = {"github" : "github_queue", "gitlab" : "gitlab_queue"}

def user_callback(ch, method, properties, body):
    #print("*****body:")
    #print(body)
    user_json = body.decode()
    #print("*****user_json:")
    #print(user_json)
    user_dict = json.loads(user_json)
    #print("*****user_dict:")
    #print(user_dict)
    r.set("User:{}".format(user_dict["email"]), user_json)
    schedule.every(periods[user_dict['period']]).days.at("10:00").do(sub_ch.basic_publish, exchange='work', routing_key='scheduler_notifier_queue', body=user_dict["email"])
    for s in user_dict['subscriptions'].keys():
        for g in user_dict['subscriptions'][s]:
            sub_ch.basic_publish(exchange='work', routing_key=funcs[s], body=g)
            schedule.every(periods[user_dict['period']]).days.at("10:00").do(sub_ch.basic_publish, exchange='work', routing_key=funcs[s], body=g)

def allektamovikmovik():
        while True:
                schedule.run_pending()
                time.sleep(1)

threading.Thread(target=allektamovikmovik).start()

rest_ch.basic_consume(user_callback, queue='scheduler_queue', no_ack=True)
rest_ch.start_consuming()
