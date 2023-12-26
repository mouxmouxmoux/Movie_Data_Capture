# -*- coding: utf-8 -*-

import config
from .parser import Parser
import json

from sqlmodel import *

class Local(Parser):
    source = 'local'

    def search(self, number):
        javinfo = JavInfo()
        try:
            dic = javinfo.search(number=number)
            js = json.dumps(dic, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            return js
        except:
            db.close()
            return 404
