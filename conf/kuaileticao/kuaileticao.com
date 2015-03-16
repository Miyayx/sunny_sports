# kuaileticao_nginx.conf

# the upstream component nginx needs to connect to
#upstream django {
# server unix:///path/to/your/mysite/mysite.sock; # for a file socket
#    server 0.0.0.0:8001; # for a web port socket (we'll use this first)
#}

# configuration of the server
server {
# the port your site will be served on
    listen 80;
# the domain name it will serve for
    server_name kuaileticao.miyayx.me; # substitute your machine's IP address or FQDN
    #server_name www.kuaileticao.com kuaileticao.com; # substitute your machine's IP address or FQDN
    charset utf-8;
    access_log /var/log/nginx/kuaileticao.com/access.log;
    error_log /var/log/nginx/kuaileticao.com/error.log;

# max upload size
    client_max_body_size 75M; # adjust to taste

# Django media
    location /media {
        autoindex  on;
        alias /usr/share/nginx/sunny_sports/media;# your Django project's media files - amend as required
        }

    location /static {
        autoindex  on;
        alias /usr/share/nginx/sunny_sports/static; # your Django project's static files - amend as required
    }

# Finally, send all non-media requests to the Django server.
    location / {
        #autoindex  on;
        #root /home/kltc/Project/sunny_sports/sunny_sports;
        #index index.html login.html;
        #uwsgi_pass django; #django可以看做变量，在上面有值
        uwsgi_pass 127.0.0.1:8002; #django可以看做变量，在上面有值
        include uwsgi_params; # the uwsgi_params file you installed
    }
}
