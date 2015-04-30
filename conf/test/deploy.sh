#!/bin/sh

#cp kuaileticao.miyayx.me /etc/nginx/sites-available/
#ln -s /etc/nginx/sites-available/kuaileticao.miyayx.me /etc/nginx/sites-enabled/

#mkdir /var/log/nginx
#mkdir /var/log/nginx/kuaileticao.miyayx.me
#mkdir /var/log/celery
#mkdir /var/run/celery
#chown -R kltc:kltc /var/log/celery
#chown -R kltc:kltc /var/run/celery

rm /etc/sysconfig/celery_test
rm /etc/sysconfig/celerybeat_test
rm /etc/systemd/system/celery_test.service
rm /etc/systemd/system/celerybeat_test.service
ln -s /home/kltc/Project/sunny_sports/conf/test/celery_test /etc/sysconfig/
ln -s /home/kltc/Project/sunny_sports/conf/test/celerybeat_test /etc/sysconfig/
ln -s /home/kltc/Project/sunny_sports/conf/test/celery_test.service /etc/systemd/system/
ln -s /home/kltc/Project/sunny_sports/conf/test/celerybeat_test.service /etc/systemd/system/

#systemctl daemon-reload
#systemctl restart nginx
#systemctl restart celery_test
#systemctl enable celery_test
#systemctl restart celerybeat_test
#systemctl enable celerybeat_test
