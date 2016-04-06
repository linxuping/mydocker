FROM ubuntu
MAINTAINER Kavin
#RUN apt-get update
RUN apt-get install -y python
#RUN apt-get install -y -q python-pip
ADD pip.py /opt/pip.py
WORKDIR /opt
RUN python pip.py
RUN pip install setuptools
RUN pip install django
RUN django-admin.py startproject mysite
ADD run.sh /opt/mysite/run.sh
WORKDIR /opt/mysite
RUN chmod 777 run.sh
EXPOSE 8080
CMD ["/bin/sh","run.sh"]

