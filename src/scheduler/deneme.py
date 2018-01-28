import threading,schedule, time

def fikibok():
	print("fikibok")

def allektamovikmovik(): 
	while 1:
		schedule.run_pending()
		time.sleep(1)

schedule.every(0.1).minutes.do(fikibok)
threading.Thread(target=allektamovikmovik).start()

while True:
	print("main: şimdilik boş boş takılıyorum")
	time.sleep(2)
