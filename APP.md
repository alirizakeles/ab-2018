# Çekiliş Robotu

Sosyal medya mecralarinda (simdilik sadece Instagram ve Twiiter) yapilan
cekilisleri otomatize eden uygulamadir.

## Servisler

### Instagram Servisi
Kullanicilar asagidaki eylemlerden birini gerceklestirerek cekilise katilabilirler.

- etkiletlemek (mention)
- begenmek

Cekilis duzenleyici hesap, `cekilis` uygulamasinin hesabini mentionlayarak kural setini asagidaki
desenlere uygun sekilde bildirir.

    @cekilis #etiket #begeni #sontarih 05.02.2016 19:00 #kazanansayisi 1
    @cekilis #begeni #sontarih 05.02.2016 19:00 #kazanansayisi 1
    @cekilis #etiket #sontarih 05.02.2016 19:00 #kazanansayisi 1


Servisimiz bu mentionlari takip eder ve cekilisi baslatir. Cekilis sonucunu ayni gonderinin altina
yazmak da servisin gorevidir. Ornek sonuc:

    #kazananlar #1 @sanslikullanici1 / #yedek #1 @jembey
    #kazananlar #1 @sanslikullanici1 #2 @anlcnydn / #yedek #1 @jembey #2 @sanssizkullanici2


### Twitter Servisi
Kullanicilar asagidaki eylemlerden birini gerceklestirerek cekilise katilabilirler.

- retweet
- begeni


Cekilis duzenleyici hesap, takip edilecek tweete yanit olarak gonderecegi
cevap icinde `cekilis` uygulamasinin hesabini mentionlar ve kural setini de asagidaki desenlere
uygun sekilde bildirir.

    @cekilis #mention #retweet #begeni #sontarih 05.02.2016 19:00 #kazanansayisi 1
    @cekilis #begeni #sontarih 05.02.2016 19:00 #kazanansayisi 1
    @cekilis #mention #sontarih 05.02.2016 19:00 #kazanansayisi 1
    @cekilis #retweet #begeni #sontarih 05.02.2016 19:00 #kazanansayisi 1

Servisimiz bu mentionlari takip eder ve cekilisi baslatir. Cekilis sonucunu ayni gonderinin altina
yazmak da servisin gorevidir. Ornek sonuc:

    #kazananlar #1 @sanslikullanici1 / #yedek #1 @jembey
    #kazananlar #1 @sanslikullanici1 #2 @anlcnydn / #yedek #1 @jembey #2 @sanssizkullanici2


### Zamanlayici Servisi
Bu servis, yeni gelen cekilisleri zamanlar ve cekilis zamani geldiginde ilgili servisleri harekete gecirir.


### Cekilis Servisi
Bu servis, cekilis katilimcilarini ve cekilis kurallarini veritabanindan okur, cekilisi yapar ve sonucu
bildirmek uzere ilgili servise iletir.



