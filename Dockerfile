FROM python:3.9.4-buster

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]



#   pip freeze > requirements.txt
#   docker build -t artrecommenderdocker .
#   docker run artrecommenderdocker
#   docker  run -it artrecommenderdocker /bin/bash
#   docker system prune
#   docker rmi $(docker images --filter “dangling=true” -q --no-trunc)