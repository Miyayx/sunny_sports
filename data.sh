#!/bin/bash
#python manage.py dumpdata sp --indent 2 --format json > data.json
python manage.py sqlclear sp > sql
sed -i '2i SET FOREIGN_KEY_CHECKS=0;' sql
N=`cat sql | wc -l`
$N=$(($N-1))
sed -i "${N}i SET FOREIGN_KEY_CHECKS=1;" sql
cat sql | python manage.py dbshell
python manage.py syncdb
#python manage.py loaddata data.json

