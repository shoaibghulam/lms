FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
<<<<<<< HEAD
COPY . /code/
=======
COPY . /code/
>>>>>>> d74b6bc3db17185c004e218a9f128153c1a5245d
