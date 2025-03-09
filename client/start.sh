#!/bin/bash

str=$"\n"

cd /home/linux1/mysite/client
nohup node client.js > /dev/null 2>&1 &

sstr=$(echo -e $str)
echo $sstr