# -*-  coding: utf-8 -*-
import os
from convert import converter
from pyoko.exceptions import ObjectDoesNotExist
from ulakbus.models.personel import *
from .orcl import Orcl

DB_USER = os.getenv("DB_USER", None)
DB_PASS = os.getenv("DB_PASS", None)
DB_HOST = os.getenv("DB_HOST", None)


orcl = Orcl(DB_USER, DB_PASS, DB_HOST)
orcl.get_cursor()
orcl.cursor.execute("SELECT p.*, SUPEBS.ALTBIRIMNOGETIR(p.vatandaslikno,1) as BIRIMNO,SUPEBS.UNVANGETIR(p.vatandaslikno) as UNVAN FROM SUPEBS.PERSONEL p")

insert = 0
update = 0

for row in orcl.rows_as_dicts():
    tckn = row['VATANDASLIKNO']
    try:
        personel = Personel.objects.get(tckn=tckn)
        update += 1
    except ObjectDoesNotExist:
        personel = Personel(tckn=tckn)
        insert += 1

    data, err = converter("PERSONEL", row)

    personel.data.extend(data)
    # personel.save()
