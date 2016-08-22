#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from data_map import PERSONEL, OGRENCI, BIRIM

def converter(tname, requests):
    if(tname=='PERSONEL'):
        dmap = dict(PERSONEL)
    elif(tname=='OGRENCI'):
        dmap = dict(OGRENCI)

    ret = {}
    error = {}
    for req in requests:
        data = dmap[req]
        if data == '':
            error[req] = requests[req]
        else:
            ret[data] = requests[req]
    return ret, error

def convert_unit(birim_id):
    birim_map = dict(BIRIM)
    if birim_id:
        birim_id = str(int(birim_id))

        if birim_id in birim_map:
            return birim_map[birim_id]
        else:
            print birim_id
            return None
    else:
        return None