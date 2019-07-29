#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2017 zenbook <zenbook@zenbook-XPS>
# Copyright (c) 2019 a2c <a2cgle@gmail>
#
# Distributed under terms of the MIT license.
#

from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask_sockets import Sockets
import redis
import threading
import gevent
import json
import os

from env import *

app = Flask(__name__)
if DEVFLG:
  app.debug = True
sockets = Sockets(app)
client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

class MessageServer(object):
  def __init__(self):
    self.clients = list()
    self.pubsub = client.pubsub()
    self.pubsub.subscribe( REDIS_CHANNEL )

  def __iter_data(self):
    for message in self.pubsub.listen():
      data = message.get('data')
      if message['type'] == 'message':
        data = json.loads(data)
        app.logger.info(u'Sending message: {}'.format(data))
        yield json.dumps(data, indent = 2, ensure_ascii = False)

  def register(self, client):
    self.clients.append(client)

  def send(self, client, data):
    try:
      client.send(data)
    except Exception:
      self.clients.remove(client)

  def run(self):
    for data in self.__iter_data():
      for client in self.clients:
        self.send(client, data)

  def start(self):
    self.run()

ms = MessageServer()

@app.route('/favicon.ico')
def favicon():
  return send_from_directory( os.path.join(app.root_path, 'templates'),
      'favicon.svg',
      mimetype='image/svg+xml')

@sockets.route('/channel')
def echo_socket(ws):
  ms.register(ws)
  while not ws.closed:
    gevent.sleep(0.1)

@app.route('/')
def index():
  data = {"FLASK_PORT":FLASK_PORT}
  return render_template('index.html', data = data)

if __name__ == "__main__":
  from gevent import pywsgi
  from geventwebsocket.handler import WebSocketHandler
  t = threading.Thread(target=ms.start)
  t.daemon = True
  t.start()
  #ms.start()
  if DEVFLG:
    print( "WSGI Server starts. port:%s"%(FLASK_PORT))
  server = pywsgi.WSGIServer(('', FLASK_PORT), app, handler_class=WebSocketHandler)
  server.serve_forever()
