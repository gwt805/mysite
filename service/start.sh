#!/bin/bash

str=$"\n"

cd /home/linux1/mysite/server
export APP_ID=102111858
export BOT_SECRET=cXSNIEA62yurolifcZXVTRPNMLKJIHGG
nohup /home/linux1/anaconda3/bin/python manage.py runserver 0.0.0.0:8080 --nothreading > /dev/null 2>&1 &

sstr=$(echo -e $str)
echo $sstr