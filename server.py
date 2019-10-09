#!/usr/bin/python3

# sudo apt-get install python3-pip
# sudo pip3 install flask

import os
from flask import Flask, request, Response
from multiprocessing import Pool
from parser import ChProcess
import json
import datetime

app = Flask(__name__)
port = 80 if os.getuid() == 0 else 8000

pool = Pool(1, maxtasksperchild=50)

parse = ChProcess('en_core_web_sm')


@app.route('/', methods=['POST', 'GET'])
def index():
  data = request.data.decode('utf-8')
  if not data:
    return Response(status=500, response="no data")

  print("got something: '%s'" % data)
  print(datetime.datetime.utcnow())
  # result = pool.apply(parse.to_json, [data, request.args])
  result = parse.to_json(data, request.args)
  print(datetime.datetime.utcnow(), 'fin')

  return Response(
      status=200, response=json.dumps(result), content_type="application/json")


if __name__ == '__main__':
  app.run(port=port, host="0.0.0.0")
