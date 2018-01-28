import schedule, time

def fikibok():
	print("fikibok")

def allektamovikmovik():
	print("hello from func 2")

schedule.every(0.1).minutes.do(fikibok)
schedule.every().day.at("10:12").do(allektamovikmovik)

while True:
	schedule.run_pending()
	time.sleep(1)
