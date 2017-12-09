FROM ubuntu
MAINTAINER Kavin

# Set Locale
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

#RUN apt-get update
RUN echo deb http://archive.ubuntu.com/ubuntu precise universe multiverse >> /etc/apt/sources.list; apt-get update; apt-get -y install autoconf automake build-essential git mercurial cmake libtool pkg-config wget python 
#RUN apt-get install -y python-dev libxml2-dev libxslt1-dev zlib1g-dev python-yaml #django env. 

ADD pip.py /opt/pip.py
WORKDIR /opt
RUN python pip.py
RUN pip install setuptools
RUN pip install tornado
EXPOSE 9900

#VOLUME /mnt   #error place: later commands can not change 'VOLUME'
#ADD script/build.sh /build.sh
#RUN chmod 777 /build.sh
#RUN ["/bin/bash", "/build.sh"]
#CMD ["/bin/sh","run.sh"]
#CMD ["/bin/bash"]

#VOLUME /mnt
#WORKDIR /mnt
RUN apt-get clean



