#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2017 zenbook <zenbook@zenbook-XPS>
# Copyright (c) 2019 a2c <a2cgle@gmail>
#
# Distributed under terms of the MIT license.
#

import redis
import time
import json
from random import randint
from env import *

dummy_data = {
  "version":"0.01",
  "telop_count":"1",
  "telops":[
    {
      "telop_type":"foofoo",
      "text_count": "1",
      "text_types":[
        {
          "text_type": "1",
          "text_data":[
            {
              "id": "20190729 ",
              "text": "hogehoge",
              "confidence" : "0.800",
              "detect_text": "fugafuga",
              "distance": "1",
              "b_box":{
                "xs": "239",
                "ys": "116",
                "xe": "622",
                "ye": "166"
              }
            }
          ]
        }]
    }
  ]
}

if __name__ == '__main__':
  client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
  pubsub = client.pubsub()
  pubsub.subscribe(REDIS_CHANNEL)
  cnt = 0
  while True:
    dummy_data['telop_count'] = cnt
    pub_json = json.dumps(dummy_data, ensure_ascii=False)

    print( pub_json )
    client.publish(REDIS_CHANNEL, pub_json)
    time.sleep(1)
    cnt += 1
