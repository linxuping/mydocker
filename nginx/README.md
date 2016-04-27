http {

        ##
        # Basic Settings
        ##
        upstream diff_subnet {
                server 192.168.221.128:9999;
                server 192.168.221.101:9999;
                server 10.10.2.2:9999;
        }

        server {
                listen 8080;
                location / {
                        proxy_pass http://diff_subnet;
                }
        }
	... ...
}
servers:
nc -l 192.168.221.128 9999;
nc -l 192.168.221.101 9999;
nc -l 10.10.2.2 9999;


rules to ports 64000*n:
server addr1:9999
server addr2:9999
nc -l addr1 9999;
nc -l addr2 9999;

cmds:
nginx -c .../nginx.conf
nginx -s reload


