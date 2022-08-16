#!/bin/bash

cd /home/ec2-user/papamobile-crawler
/home/ec2-user/.local/bin/scrapy crawl otomoto &>/home/ec2-user/scrapy.log &

cd transform
./venv/bin/python3 ./transform.py &>/home/ec2-user/transform.log &

