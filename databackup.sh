#!/bin/bash

#projectpath='/home/kltc/Project/sunny_sports/sunny_sports/'
projectpath='/usr/share/nginx/sunny_sports/'
backuppath='/home/kltc/kuaileticao/'
#database='sunny_sports'
database='kuaileticao'

datename=$(date +%Y%m%d%H%M%S) #文件名按时间命名
mkdir /home/kltc/kuaileticao/
mkdir /home/kltc/kuaileticao/mediabackup/
mkdir /home/kltc/kuaileticao/sqlbackup/

tar zcvf ${backuppath}mediabackup/media.${datename}.tar.gz ${projectpath}media/ #备份压缩网站的图片文件夹 
sqlbackupname=${backuppath}sqlbackup/mysql.${datename}
#/usr/bin/mysqldump -uqueen -pdorm $database > ${sqlbackupname}.sql #从数据库备份数据
/usr/bin/mysqldump $database > ${sqlbackupname}.sql #从数据库备份数据
tar zcvf ${sqlbackupname}.tar.gz ${sqlbackupname}.sql 
rm -rf ${sqlbackupname}.sql

#还原
#/usr/bin/mysql -uqueen -p $database < db_name.sql
