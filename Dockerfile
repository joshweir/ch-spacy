FROM python:3.6

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    supervisor \
    curl \
    nginx \
    python-dev \
    git &&\
    apt-get -q clean -y && rm -rf /var/lib/apt/lists/* && rm -f /var/cache/apt/*.bin

RUN pip install spacy==2.1.0

RUN python -m spacy download en_core_web_sm

RUN pip install neuralcoref

ENV NEURALCOREF_CACHE=/neuralcoref-cache
RUN mkdir /neuralcoref-cache
RUN (cd /neuralcoref-cache && curl -O https://s3.amazonaws.com/models.huggingface.co/neuralcoref/neuralcoref.tar.gz) &&\
  mv /neuralcoref-cache/neuralcoref.tar.gz /neuralcoref-cache/f46bc05a4bfba2ae0d11ffd41c4777683fa78ed357dc04a23c67137abf675e14.7d6f9a6fecf5cf09e74b65f85c7d6896b21decadb2554d486474f63b95ec4633 &&\
  cd

# RUN git clone https://github.com/explosion/spaCy
# RUN git clone https://github.com/huggingface/neuralcoref.git

# # RUN python -m venv .env
# # RUN . .env/bin/activate
# WORKDIR /spaCy
# RUN pip install -r requirements.txt
# RUN python setup.py build_ext --inplace
# RUN python setup.py install

# WORKDIR /neuralcoref
# RUN python -m venv /spaCy/.env
# RUN . /spaCy/.env/bin/activate
# RUN python -m spacy validate
# RUN pip install -r requirements.txt
# RUN pip install -e .
# RUN python setup.py build_ext --inplace
# RUN python setup.py install

# WORKDIR /root

# CMD bash

WORKDIR /

COPY ./requirements.txt /
RUN pip install -r requirements.txt

# ENV NLP_ARCHITECT_BE=CPU
# RUN pip install nlp-architect

# RUN python -m spacy download en_core_web_sm
# ENV NEURALCOREF_CACHE=/neuralcoref-cache
# RUN mkdir /neuralcoref-cache
# RUN (cd /neuralcoref-cache && curl -O https://s3.amazonaws.com/models.huggingface.co/neuralcoref/neuralcoref.tar.gz) &&\
#   mv /neuralcoref-cache/neuralcoref.tar.gz /neuralcoref-cache/f46bc05a4bfba2ae0d11ffd41c4777683fa78ed357dc04a23c67137abf675e14.7d6f9a6fecf5cf09e74b65f85c7d6896b21decadb2554d486474f63b95ec4633 &&\
#   cd

ADD ./ /app

WORKDIR /app

CMD gunicorn --bind 0.0.0.0:80 \
  --worker-tmp-dir /dev/shm \
  --workers=2 --threads=4 --worker-class=gthread \
  --log-file=- \
  --preload \
  wsgi:app
