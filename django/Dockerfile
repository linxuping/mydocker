FROM ubuntu:14.04
MAINTAINER Kavin

# Set Locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

#RUN apt-get update
RUN apt-get install -y python git
ADD pip.py /opt/pip.py
WORKDIR /opt
RUN python pip.py
RUN pip install setuptools
RUN pip install django==1.9.5
RUN django-admin.py startproject mysite
ADD run.sh /opt/mysite/run.sh
WORKDIR /opt/mysite
RUN chmod 777 run.sh
EXPOSE 9900

#VOLUME /mnt   #error place: later commands can not change 'VOLUME'
ADD script/build.sh /build.sh
RUN chmod 777 /build.sh
RUN ["/bin/bash", "/build.sh"]
VOLUME /mnt

CMD ["/bin/sh","run.sh"]
#CMD ["/bin/bash"]


