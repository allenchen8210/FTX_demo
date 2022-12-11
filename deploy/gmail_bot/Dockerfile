FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt ./
#RUN apk add g++
RUN apk add \
#    wget \
    g++ \
    gcc \
#    make \
#    zlib-dev  \
    libffi-dev \
#    openssl-dev \
    musl-dev

#RUN pip3 install --upgrade setuptools
#RUN pip3 install Cmake
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 6000
#RUN export FLASK_APP=flask_request.py
#CMD [ "python3", "mysql_interface.py" ]
#CMD [ "python3", "flask_request.py"]
CMD [ "python3", "gmail_bot.py"]