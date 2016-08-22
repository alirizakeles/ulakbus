# -*-  coding: utf-8 -*-
import os
from convert import converter, convert_unit
from pyoko.exceptions import ObjectDoesNotExist
from ulakbus.models.personel import *
from orcl import Orcl

DB_USER = os.getenv("DB_USER", None)
DB_PASS = os.getenv("DB_PASS", None)
DB_HOST = os.getenv("DB_HOST", None)

def merge_attr(model,data):
    for key in data:
        try:
            setattr(model, key, data[key])
        except Exception, e:
            pass
            # print e

orcl = Orcl(DB_USER, DB_PASS, DB_HOST)
orcl.get_cursor()

# Kadro Kopyalama
orcl.cursor.execute("SELECT k.*,k.UNVANKOD as UNVAN, (SELECT un.UNVANADI FROM SABIT.UNVANLAR un WHERE un.UNVANKOD=k.UNVANKOD) as UNVANAD FROM SUPEBS.KADRO k")

insert = 0
update = 0
atama_map = {}

for row in orcl.rows_as_dicts():
    break

    data, err = converter("PERSONEL", row)

    try:
        kadro = Kadro.objects.get(kadro_no=data['kadro_no'])
        update += 1
    except ObjectDoesNotExist:
        kadro = Kadro()
        insert += 1

        merge_attr(kadro,data)

        # AKADEMIKIDARI -> akademik 1, idari 2 için +1 eklendi
        kadro.kadro_turu += 1

        # durum
        """
          "kadro_durumlari": {
        "1": {
          "tr": "Saklı",
          "en": "Reserved"
        },
        "2": {
          "tr": "İzinli",
          "en": "Available"
        },
        "3": {
          "tr": "Bos",
          "en": "Free"
        },
        "4": {
          "tr": "Dolu",
          "en": "Occupied"
        }
      },
        """
        durum_map = {9:3,2:4,1:1,0:2}
        kadro.durum = durum_map[kadro.durum]

        # Birim map tablosundan birimi bulunacak
        birim_no =  convert_unit(err['ALTBIRIMKOD'])
        if birim_no:
            kadro.birim = Unit.objects.filter(yoksis_no=birim_no)[0]

        if kadro.izin_tarihi and kadro.izin_tarihi.year < 1900:
            kadro.izin_tarihi = None

        kadro.save()

        # personel atanmışsa mape atılıp personel oluşturduktan sonra ataması yapılacak
        if data['tckn'] != "":
            atama_map['tckn'] = kadro.key

# Personel Kopyalama
# ULKEKOD as ADRES_ULKE
orcl.cursor.execute("SELECT p.*,p.ULKEKOD as ADRES_ULKE, SUPEBS.ALTBIRIMNOGETIR(p.vatandaslikno,1) as BIRIMNO,SUPEBS.UNVANKODGETIR(p.vatandaslikno) as UNVAN, (SELECT hs.HITAPKOD FROM SUPEBS.HIZMETSINIFI hs WHERE hs.HIZMETSINIFKOD = p.HIZMETSINIFKOD) as HIZMETSINIFKOD_HITAP FROM SUPEBS.PERSONEL p")

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
        personel = Personel(tckn=tckn)
        merge_attr(personel,data)


        # kurum_sicil_no_int parse et
        personel.kurum_sicil_no_int = personel.kurum_sicil_no_int.split('-')[1]

        # personel_turu için rol ver
        # goreve_baslama_tarihi farklı tablodan doldur
        # BIRIMNO için Kadro oluşturup atama yap

        if not personel.user:
            user = User()
            user.username = personel.tckn
            user.password = "neu"
            user.name = personel.ad
            user.surname = personel.soyad
            user.save()

            personel.user = user
        print personel.clean_value()

        personel.save()
    """
    if personel.tckn in atama_map:

        atama = Atama()
        atama.personel = personel
        atama.kadro_id = atama_map[personel.tckn]

        ibraz_tarihi = field.Date("İbraz Tarihi", index=True, format="%d.%m.%Y")
        durum = HitapSebep()
        durum.title = "Durum"
        nereden = field.Integer("Nereden", index=True)  # modele baglanacak.
        atama_aciklama = field.String("Atama Açıklama", index=True)
        goreve_baslama_tarihi = field.Date("Göreve Başlama Tarihi", index=True, format="%d.%m.%Y")
        goreve_baslama_aciklama = field.String("Göreve Başlama Açıklama", index=True)
        hizmet_sinifi = field.Integer("Hizmet Sınıfı", index=True, choices="hizmet_sinifi")
    """
