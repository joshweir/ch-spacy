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

# RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_md
RUN python -m spacy link en_core_web_md en

RUN pip install neuralcoref

ENV NEURALCOREF_CACHE=/neuralcoref-cache
RUN mkdir /neuralcoref-cache
RUN (cd /neuralcoref-cache && curl -O https://s3.amazonaws.com/models.huggingface.co/neuralcoref/neuralcoref.tar.gz) &&\
  mv /neuralcoref-cache/neuralcoref.tar.gz /neuralcoref-cache/f46bc05a4bfba2ae0d11ffd41c4777683fa78ed357dc04a23c67137abf675e14.7d6f9a6fecf5cf09e74b65f85c7d6896b21decadb2554d486474f63b95ec4633 &&\
  cd

WORKDIR /

COPY ./requirements.txt /
RUN pip install -r requirements.txt

# ENV NLP_ARCHITECT_BE=CPU
# RUN pip install nlp-architect

# numpy==1.16.3
RUN pip install torch==1.0.1
RUN pip install transformers==2.0.0
RUN pip install Cython==0.29.10
RUN pip install tqdm==4.32.2
# neuralcoref==4.0
RUN pip install argparse
RUN pip install scikit-learn
RUN pip install bert-extractive-summarizer==0.2.0
RUN pip install beautifulsoup4
RUN pip install lxml

ADD ./ /app

WORKDIR /app

CMD gunicorn --bind 0.0.0.0:80 \
  --worker-tmp-dir /dev/shm \
  --workers=2 --threads=4 --worker-class=gthread \
  --log-file=- \
  --preload \
  wsgi:app
