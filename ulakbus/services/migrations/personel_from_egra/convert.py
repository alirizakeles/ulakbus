#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def converter(tname, requests):
    with open("personel") as json_file:
        json_data = json.load(json_file)
    ret = {}
    error = {}
    for req in requests:
        data = json_data[tname][req]
        if data == '':
            error[req] = requests[req]
        else:
            ret[data] = requests[req]
    return ret, error
