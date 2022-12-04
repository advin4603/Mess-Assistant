FROM python:3.8

WORKDIR /assistant

RUN pip install --no-cache-dir rasa

RUN pip install --no-cache-dir requests

RUN pip install --no-cache-dir beautifulsoup4

RUN pip install lxml

COPY . /assistant

ENTRYPOINT [ "rasa" ]
