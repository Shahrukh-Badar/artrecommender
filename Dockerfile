FROM python:3.9.4-buster

# copy the dependencies file to the working directory
COPY requirements.txt /

# install dependencies
RUN pip install -r requirements.txt

# Copy source code
COPY . /
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]
# Run the application
#CMD ["python", "main.py"]


#   pip freeze > requirements.txt
#   docker build -t artrecommenderdocker .
#   docker run artrecommenderdocker
#   docker  exec -it artrecommenderdocker /bin/bash