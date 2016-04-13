_path=`pwd`/django_composite
docker run -it -p 9900:9900 -v $_path:/mnt ubuntu:django /bin/bash

