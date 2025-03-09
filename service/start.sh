#!/bin/bash

str=$"\n"

cd /home/linux1/mysite/server
nohup /home/linux1/anaconda3/bin/python manage.py runserver 0.0.0.0:8080 --nothreading > /dev/null 2>&1 &

sstr=$(echo -e $str)
echo $sstr