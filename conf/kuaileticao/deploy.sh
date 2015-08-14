#!/bin/sh

#cp kuaileticao.com /etc/nginx/sites-available/
#ln -s /etc/nginx/sites-available/kuaileticao.com /etc/nginx/sites-enabled/

#mkdir /var/log/nginx
#mkdir /var/log/nginx/kuaileticao.com
#mkdir /var/log/celery
#mkdir /var/run/celery
#chown -R kltc:kltc /var/log/celery
#chown -R kltc:kltc /var/run/celery


rm /etc/sysconfig/celery
#rm /etc/sysconfig/celerybeat
rm /etc/systemd/system/celery.service
ln -ns `pwd`/celery /etc/sysconfig/
#ln -ns `pwd`/celerybeat /etc/sysconfig/
ln -ns `pwd`/celery.service /etc/systemd/system/
#ln -ns `pwd`/celerybeat.service /etc/systemd/system/

systemctl daemon-reload
#systemctl restart nginx
systemctl restart celery
systemctl enable celery
#systemctl restart celerybeat
#systemctl enable celerybeat
