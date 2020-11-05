#!/usr/bin/env python
# -*- coding:utf-8 -*-


from common import app

from douyin import controller

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s [%(filename)s-%(lineno)d]')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
