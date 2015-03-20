#!/bin/sh

ln -nsf `pwd`/kuaileticao/uwsgi.ini /etc/uwsgi/vassals/kuaileticao.uwsgi.ini
ln -nsf `pwd`/test/uwsgi.ini /etc/uwsgi/vassals/kuaileticao_test.uwsgi.ini
cp emperor.ini /etc/uwsgi/
cp uwsgi.service /etc/systemd/system/
systemctl daemon-reload
systemctl restart uwsgi
systemctl enable uwsgi

cd `pwd`/kuaileticao
sh deploy.sh
#cd `pwd`/test
#sh deploy.sh
