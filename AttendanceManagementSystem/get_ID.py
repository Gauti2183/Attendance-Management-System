#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 15:03:04 2018

@author: uhong
"""

import requests
url = 'http://192.168.1.7'
def get_ID():
    try:
        res = requests.get(url,timeout=0.5)
        return res.text
    except:
        return "Connection Filed"