# Python ile Mikroservis Mimarisinde Uygulama Geliştirme
## Genel İzlek
Aşağıda adı geçen konular ile paralel bir uygulama geliştirilecektir. Konularla birlikte adım adım  ilerlenecek ve kursun sonunda çalışan bir uygulamaya sahip olunacaktır.
- Mikroservis nedir?
- Neden mikroservis mimarisi?
    - avantajları
    - Dezavantajları
- Mikroservis mimarisi ve REST?
- Servislerin planlanması
- Servisler arası iletişim nasıl sağlanır?
    - rpc
    - http
    - websockets
- Deployment çözümleri
Örnek uygulama tekil servisler ve elle yapılandırılmış deployment parametreleri ile  gerçekleşecek, daha karmaşık, yüksek bulunurluklu, ölçeklenebilir senaryolar hakkında bilgi verilecek ve sorular yanıtlanacaktır.
    - Konteynerlaştırmak (containerization) ne faydalar sağlar?
    - Service discovery. Servislerin keşfedilmesi ve ilgili yerlere bildirilmesi / kaydedilmesi
    - Servislerin izlenmesi (health check)

## Değinilecek Konular

### Python
- python ile asenkron / eş zamanlı yazılım pratikleri
- threading, multiprocessing
- queues
- event loops
- python ile rest framework
- python ile JWT

### Redis
- KV veritabanları ve Redis
- Veri yapıları
- Mikroservislerle kullanmak için Redis üzerinde
    - iş kuyrukları
    - pub / sub
    - geçici veri depolama stratejileri

### RabbitMQ
- Protokol AMQP
- Temel kavramlar
    - Exchange
    - Queues
- RabbitMQ client Pika
- Blocking / Non-blocking bağlantı türleri

### Docker
- Temel kavramlar ve temel komutlar
- Docker compose ile servislerin birlikte çalıştırılması


### Örnek Uygulama
Bu konuları kapsayan örnek uygulama.

### Katılımcılardan Beklenenler
- Temel GNU/Linux bilgisi
- Temel Python bilgisi
- Temel veri yapıları bilgisi
- Katılımcıların bilgisayarlarında Python 3.6 versiyonun kurulu olması
- Katılımcıların bilgisayarlarında Docker servisinin kurulu olması
- Katılımcıların biglisayarlarında Redis ve Rabbitmq docker servislerinin çalışır olması gerekmektedir. 
