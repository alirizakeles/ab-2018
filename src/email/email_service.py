import json
import os
import smtplib
import time

import redis

'''try:
    email_user_name = os.environ["EMAIL_USER"]
    email_user_pass = os.environ["EMAIL_PASS"]
except KeyError:
    raise Exception("Please set environment variables EMAIL_USER and EMAIL_PASS")

r = redis.Redis()
job = b'{"to":"anlcnydn@gmail.com", "stars": ["repo1", "repo2"]}'
json.loads(job.decode())

job_queue = "email_queue"'''


def send_email(receiver, body):
    email_user_name = "abkurs@sifirbir.xyz"
    email_user_pass = "cokcokcokgizli"

    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (email_user_name, receiver, "Star reminder", body)

    server = smtplib.SMTP('box.sifirbir.xyz', 587)
    server.ehlo()
    server.starttls()

    server.login(user=email_user_name, password=email_user_pass)
    senderss = server.sendmail(from_addr=email_user_name, to_addrs=receiver, msg=email_text)
    print (senderss)
    server.close()

if __name__ == '__main__':
    send_email("ali@sifirbir.xyz", "ne haber")

    while True:
        job = r.rpop(job_queue)
        new_email = json.loads(job)
        try:
            send_email(new_email['to'], "\n".join(new_email["stars"]))
        except:
            r.lpush(job)

        time.sleep(10)
