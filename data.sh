#!/bin/bash
#python manage.py dumpdata sp --indent 2 --format json > data.json
python manage.py sqlclear sp| python manage.py dbshell
python manage.py syncdb
python manage.py loaddata data.json

