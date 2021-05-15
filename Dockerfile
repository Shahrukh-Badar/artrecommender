FROM python:3.9.4-buster

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
