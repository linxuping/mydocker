FROM ubuntu:14.04

MAINTAINER Joshua Gardner mellowcellofellow@gmail.com

# Set Locale

RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8



# Enable Universe and Multiverse and install dependencies.

RUN echo deb http://archive.ubuntu.com/ubuntu precise universe multiverse >> /etc/apt/sources.list; apt-get update; apt-get -y install autoconf automake build-essential git mercurial cmake libass-dev libgpac-dev libtheora-dev libtool libvdpau-dev libvorbis-dev pkg-config texi2html zlib1g-dev libmp3lame-dev wget yasm; apt-get clean
RUN apt-get install -y python python-pip psmisc;pip install pika

# Run build script

ADD script/build.sh /build.sh
RUN ["/bin/bash", "/build.sh"]
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && ntpdate cn.pool.ntp.org
RUN echo "chmod +x /mnt/run.sh;cd /mnt;./run.sh">>/etc/bash.bashrc

CMD ["/bin/bash"]
WORKDIR /mnt

