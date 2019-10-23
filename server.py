#!/usr/bin/python3

# sudo apt-get install python3-pip
# sudo pip3 install flask

import os
from flask import Flask, request, Response
from parser import ChProcess, TextClean
import json
import datetime
from summarizer import Summarizer
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
port = 80 if os.getuid() == 0 else 8000

parse = ChProcess('en_core_web_sm')
text_cleaner = TextClean()
# default model: bert-large-uncased
summrizer = Summarizer(model='distilbert-base-uncased', greedyness=0.45)


@app.route('/', methods=['POST', 'GET'])
def index():
  data = request.data.decode('utf-8')
  if not data:
    return Response(status=500, response="no data")

  print("got something: '%s'" % data)
  print(datetime.datetime.utcnow())
  result = parse.to_json(data, request.args)
  print(datetime.datetime.utcnow(), 'fin')

  return Response(
      status=200, response=json.dumps(result), content_type="application/json")


@app.route('/text-clean', methods=['POST', 'GET'])
def text_clean():
  data = request.data.decode('utf-8')
  if not data:
    return Response(status=500, response="no data")

  print("got something to clean: '%s'" % data)
  print(datetime.datetime.utcnow())

  result = text_cleaner.call(data) + '\n'
  print(datetime.datetime.utcnow(), 'fin')

  return Response(status=200, response=result)


@app.route('/summarize', methods=['POST', 'GET'])
def summarize():
  data = request.data.decode('utf-8')
  if not data:
    return Response(status=500, response="no data")

  print("got something to summarize: '%s'" % data)
  print(datetime.datetime.utcnow())

  has_markup = re.match(r'<[^>]*>', data) or re.match(r'&[A-Za-z]+;', data)
  if has_markup:
    data = BeautifulSoup(data, 'lxml').get_text()
    print("has markup, transformed: %s" % data)

  result = summrizer(data, result_format='array', num_sentences=3)
  print(datetime.datetime.utcnow(), 'fin')

  return Response(status=200, response=result, content_type="application/json")


if __name__ == '__main__':
  app.run(port=port, host="0.0.0.0")
