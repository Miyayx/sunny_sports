#!/bin/sh

cp kuaileticao.miyayx.me /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/kuaileticao.miyayx.me /etc/nginx/sites-enabled/

mkdir /var/log/nginx
mkdir /var/log/nginx/kuaileticao.miyayx.me
mkdir /var/log/celery
mkdir /var/run/celery
chown -R kltc:kltc /var/log/celery
chown -R kltc:kltc /var/run/celery

#cp celery_test /etc/sysconfig/
#cp celerybeat_test /etc/sysconfig/
cp uwsgi.ini /etc/uwsgi/kuaileticao_test.uwsgi.ini
chmod 664 /etc/uwsgi/kuaileticao_test.uwsgi.ini
cp kuaileticao_test.service /etc/systemd/system/
#cp celery_test.service /etc/systemd/system/
#cp celerybeat_test.service /etc/systemd/system/

systemctl restart kuaileticao_test
systemctl enable kuaileticao_test
systemctl restart nginx
#systemctl restart celery_test
#systemctl enable celery_test
#systemctl restart celerybeat_test
#systemctl enable celerybeat_test
