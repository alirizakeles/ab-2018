import threading, schedule
from time import sleep
import redis
import json

redis_cli = redis.Redis()
sample_data = """{
	'email': 'tunahan@dursun.com',
	'repoCount':2,
	'period':'weekly',
	'telegramId':'asdf',
	'subscriptions':{
		'github':['anilaydin'],
		'gitlab':['aliriza']
	}
}"""
# Bu kod parçacığı, rabitten okuduğu veriyi,  redise yazar ve workerlara iş bırakır.

def schedleri_ayarla(kullanici_verisi):
	# redise veriler yazıldıktan sonra workerlardan starları çekecek olan workerlara rabbit üzerinden 
	# veri bırakır. notifiera iş bırakmayacak.
	period = kullanici_verisi['period']

	if period == "daily":
		schedule.every(1).days.at("10:10").do(notifiera_is_birak)

	else if period ==  "weekly":
		schedule.every(7).days.at("10:10").do(notifiera_is_birak)

	else if period == "monthly":
		schedule.every(30).days.at("10:10").do(notifiera_is_birak)

def redise_yazdir(kullanici_verisi):
	# rabitten okunan veriler, redise kaydediliyor
	redis_cli.set(':'.join(["User",kullanici_verisi['email']],json.dumps(kulanici_verisi))

def tempi_sil(kullanici_verisi):
	# rediste bulunan, kullanıcıya ait verilerin bulunduğu datayı redisten siliyor
	redis_cli.delete(":".join(["temp","User",kullanici_verisi['email']])) 

def notifiera_is_birak():
	# Kullanıcılara eposta yollanması için gerekli iş notifieara bırakılacak
	pass

def workerlara_starlari_denetlet():
	# Kaydı oluşturulan kullacıların starlarının zaman zaman denetlenmesi sağlanıcak
	pass

def allektamovikmovik(): 
	while 1:
		schedule.run_pending()
		time.sleep(1)

threading.Thread(target=allektamovikmovik).start()

while True:
	# Burası rabiti dinleyecek. Yeni bir kullanıcı eklendiğinde ilgili fonksiyonlar çalıştırılacak 
	# rabitten sample_data verisinin geldiği varsayılıyor
	kullanici_verisi = json.loads(sample_data)

	redise_yazdir(kullanici_verisi)
	schedleri_ayarla(kullanici_verisi)
	tempi_sil(kullanici_verisi)

	time.sleep(2)

