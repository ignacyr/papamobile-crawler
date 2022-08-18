#!/bin/bash

cd /home/ec2-user/papamobile-crawler
/home/ec2-user/.local/bin/scrapy crawl otomoto &>/home/ec2-user/scrapy.log

/usr/bin/python3 /home/ec2-user/papamobile-crawler/transform/transform.py &>/home/ec2-user/transform.log

