#!/bin/bash
source /home/ken/pttCrawler/env/bin/activate 
/home/ken/pttCrawler/env/bin/python /home/ken/pttCrawler/main.py >> /home/ken/pttCrawler/logfile.log 2>&1
deactivate