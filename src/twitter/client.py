from __future__ import print_function

import os
import twitter
from ..common import cekilis_mesaji_kontrol, cekilis_baslat

consumer_key = os.getenv("TWITTER_CONSUMER_KEY", None)
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET", None)
access_token = os.getenv("TWITTER_ACCESS_TOKEN", None)
access_secret = os.getenv("TWITTER_ACCESS_SECRET", None)

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_secret)


def yeni_cekilis_kontrol_et():
    for status in api.GetMentions():
        status = api.GetStatus(status.id)
        cekilis = cekilis_mesaji_kontrol(status["text"])
        if cekilis:
            cekilis_baslat("twitter", status["in_reply_to_status_id"], cekilis)


def sonuc_acikla():
    pass
