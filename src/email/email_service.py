import os
import smtplib


'''try:
    email_user_name = os.environ["EMAIL_USER"]
    email_user_pass = os.environ["EMAIL_PASS"]
except KeyError:
    raise Exception("Please set environment variables EMAIL_USER and EMAIL_PASS")

r = redis.Redis()
job = b'{"to":"anlcnydn@gmail.com", "stars": ["repo1", "repo2"]}'
json.loads(job.decode())

job_queue = "email_queue"'''

EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST")
EMAIL_SMTP_PORT = os.getenv("EMAIL_SMTP_PORT")


def send_email(receiver, body):
    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (EMAIL_USERNAME, receiver, "Star reminder", body)

    server = smtplib.SMTP(EMAIL_SMTP_HOST, EMAIL_SMTP_PORT)
    server.ehlo()
    server.starttls()

    server.login(user=EMAIL_USERNAME, password=EMAIL_PASSWORD)
    senderss = server.sendmail(from_addr=EMAIL_USERNAME, to_addrs=receiver,
                               msg=email_text)
    print(senderss)
    server.close()
