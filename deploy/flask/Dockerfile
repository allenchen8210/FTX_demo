FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt ./
#RUN apk add g++
RUN apk add \
#    wget \
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

EXPOSE 5000
#RUN export FLASK_APP=flask_request.py
#CMD [ "python3", "mysql_interface.py" ]
#CMD [ "python3", "flask_request.py"]
CMD [ "python3", "flask_request.py", "--site_path", "/usr/local/lib/python3.8/site-packages"]


#FROM python:3.9-alpine as base
#FROM base as builder
#COPY requirements.txt /requirements.txt
#RUN pip install --user -r /requirements.txt
#
#FROM base
## copy only the dependencies installation from the 1st stage image
#COPY --from=builder /root/.local /root/.local
#COPY . /app
#WORKDIR /app
#
## update PATH environment variable
#ENV PATH=/home/app/.local/bin:$PATH
#
#CMD ["/bin/sh"]