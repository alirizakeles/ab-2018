import threading, schedule
from time import sleep
# Bu kod parçacığı, rabitten okuduğu veriyi,  redise yazar ve workerlara iş bırakır.
# notifier a veri bırakır

def rabitten_oku():
	redise_yazdirmasyon()
	schedleri_ayarla()
	tempi_sil()

def schedleri_ayarla():
	# redise veriler yazıldıktan sonra workerlardan starları çekecek olan workerlara rabbit üzerinden 
	# veri bırakır. notifiera iş bırakmayacak.

	# schedule.every(5).minutes.do(workira_is_birak)
	sleep(1)
	pass

def redise_yazdirmasyon():
	# rabitten okunan veriler, redise kaydediliyor
	sleep(1)
	pass

def tempi_sil():
	# rediste bulunan, kullanıcıya ait verilerin bulunduğu datayı redisten siliyor
	sleep(1)
	pass

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

schedule.every(5).minutes.do(workira_is_birak)
threading.Thread(target=allektamovikmovik).start()

while True:
	# Burası rabiti dinleyecek. Yeni bir kullanıcı eklendiğinde rabitten_oku fonksiyonu çalıştırılacak
	print("main: şimdilik boş boş takılıyorum")
	rabitten_oku()

	time.sleep(2)

