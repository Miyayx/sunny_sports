#!/bin/bash
python manage.py dumpdata --indent 2 --format json > data.json
python manage.py sqlclear
python manage.py syncdb
python manage.py loaddata data.json

