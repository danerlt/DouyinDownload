#!/usr/bin/env python  
# -*- coding:utf-8 -*-  

import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask

logger = logging.getLogger(__name__)
fmt_str = '%(asctime)s: %(message)s [%(filename)s-%(lineno)d]'
file_log = TimedRotatingFileHandler('log', 'MIDNIGHT', interval=1, backupCount=10)
formatter = logging.Formatter(fmt_str)
file_log.setFormatter(formatter)
logger.addHandler(file_log)

app = Flask(__name__)
