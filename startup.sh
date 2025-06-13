#!/bin/bash
# git pull
nohup python main.py > service.log 2>&1 &
echo $! > pid
sleep 2
tail -200f service.log