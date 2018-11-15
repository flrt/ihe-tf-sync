FROM python:3.7
LABEL maintainer="frederic.laurent@gmail.com"

RUN pip install requests
RUN pip install html5lib
RUN pip install bs4

WORKDIR /opt
ADD *.py /opt/

VOLUME /opt
