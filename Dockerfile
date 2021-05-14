FROM python:3.9.4-buster

# copy the dependencies file to the working directory
COPY requirements.txt /

# install dependencies
RUN pip install -r requirements.txt

# Copy source code
COPY . /

# Run the application
CMD ["python", "main.py"]