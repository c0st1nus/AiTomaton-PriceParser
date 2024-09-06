FROM python:3.11-slim-buster

WORKDIR /home/const/AiTomaton-PriceParser

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y wget bzip2 && \
    apt-get install -y firefox-esr

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.32.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.32.0-linux64.tar.gz

ENV GECKODRIVER_PATH=/usr/local/bin/geckodriver
ENV FIREFOX_PATH=/usr/bin/firefox

CMD ["python3", "./main.py"]