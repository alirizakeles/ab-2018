from email_service import send_email

def listen_redis():
    send_email("example@receiver.com", "Github Stars")

if __name__ == '__main__':
    listen_redis()