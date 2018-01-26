# Rabbit MQ

Rabbit MQ GPL uyumlu Mozilla Piblic Lisansi ile dağıtılan özgür bir mesajlaşma platformudur.

Uygulamalar arasında mesajların alınması, kuyruklara dağıtılması ve alıcılara teslim edilmesi
işini yapar. Birkaç başka protokolü desteklese de, en temel ve en çok kullanılan özelliği
Advanced Message Queue Protocol (AMQP) desteğidir.

Temel olarak AMQP 0.9 desteklenmektedir. AMQP 1.0 versiyonu 0.9 dan oldukça farklılaşmıştır.
Bir eklenti ile 1.0 da desteklenmektedir.

## Temel Kavramlar

### Producer (mesaj üreten)
Trafiğin bir ucunda aşağıda daha detaylı açıklanan exchange ve/veya kuyruklara mesaj bırakan
uygulamayı belirtir. Producer, mesajı üretir ve hedefleyerek (alıcıları tarif ederek veya 
doğrudan alıcıların bağlı oldukları noktaları seçerek) bırakır.

### Consumer (mesaj tüketen)
Consumer trafiğin karşı tarafında yer alır. Platformun kendisini ilgilendiren noktalarına
abone olarak bırakılan mesajları alır.

### Exchange (takas merkezi)
Mesajların bırakıldığı ve dağıtıldığı takas merkezleridir. Producerlar exchangelere yayın
yaparak mesajların birden çok kuyruğa dağıtılmasını isteyebilirler.

4 çeşit exchange vardır:

- Direct, target selectively
- Fanout, target all audience
- Topic, target by matching a pattern
- Headers, target by amqp headers

Exchangeler aşağıdaki özellikler ile tanımlanırlar:

- Name
- Auto deletion (delete on last unbound)
- Durable (pesistent exchanges)
- Extra arguments

`Default Exchange` özel bir exchangedir. RabbitMQ'da uzerinde tanımlanan ve herhangi
başka bir exchange'e bağlanmayan kuyruklar, kuyruk isimleri `routing key` olarak kullanılarak
bu exchange'e otomatik olarak bağlanıtlar. 

Mesajlar doğrudan kuyruklara yayınlanmazlar. Exchange belirtilmemiş ise default exchange'e
gönederilirler.


### Queue (kuyruk)
Kuyruklar Producer ile Consumerlar arasında veya Exchangeler ile Consumerlar arasındaki
tamponlardır. 

### Pika
Pika AMQP 0-9-1 protokolunun Python dili implementasyonudur. Başka implementasyonlar da
mevcuttur.
