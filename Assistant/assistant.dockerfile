FROM python:3.8

WORKDIR /assistant

RUN pip install --no-cache-dir rasa

RUN pip install --no-cache-dir spacy

RUN python -m spacy download en_core_web_md

COPY . /assistant

RUN rasa train

ENTRYPOINT [ "rasa" ]
