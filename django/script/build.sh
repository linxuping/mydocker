#!/bin/bash

# Fetch Sources

cd /mnt
apt-get install -y python-dev libxml2-dev libxslt1-dev zlib1g-dev python-yaml
pip install -q jieba 
easy_install lxml
git clone https://github.com/linxuping/django_composite.git


