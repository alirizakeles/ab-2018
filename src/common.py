from datetime import datetime


def cekilis_mesaji_kontrol(mesaj):
    """

    Args:
        mesaj (str): cekilis mesaji

    Returns:
        dict: gecerli bir mesaj ise, kurallari iceren bir dict doner; aksi halde None

    ```

    In [2]: m = "@cekilis #sontarih 05.02.2016 19:00 #kazanansayisi 1 #katilim etiket begeni"
    In [3]: cekilis_mesaji_kontrol(m)
    Out[3]:
    {'katilim': ['etiket', 'begeni'],
     'kazanansayisi': ['1'],
     'sontarih': ['05.02.2016', '19:00']}

     ```

    """
    mesaj_kosullar = mesaj.split(" #")
    if len(mesaj_kosullar) != 4:
        return None
    cekilis_kosullari = {}
    for k in mesaj_kosullar:
        if k != "@cekilis":
            kosul = k.split(" ")
            if kosul[0] == "sontarih":
                try:
                    datetime.strptime("{} {}".format(kosul[1], kosul[2]), "%d.%m.%Y %H:%M")
                except ValueError:
                    return None
            cekilis_kosullari.update({kosul[0]: kosul[1:]})
    return cekilis_kosullari


def cekilis_baslat(platform, post, kurallar):
    """

    Args:
        platform (str): twitter, instagram
        post (str): post id
        kurallar (dict): cekilis kurallari

    Returns:

    """
    pass
