# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

"""HITAP IHS Sil

Hitap'da personelin IHS bilgilerinin silinmesi sağlayan class.

"""

__author__ = 'H.İbrahim Yılmaz (drlinux)'

from ulakbus.services.personel.hitap.hitap_sil import HITAPSil


class HizmetIHSSil(HITAPSil):
    """
    HITAP Silme servisinden kalıtılmış Hizmet IHS Bilgisi Silme servisi

    """

    def handle(self):
        """Servis çağrıldığında tetiklenen metod.

        Attributes:
            service_name (str): İlgili Hitap sorgu servisinin adı
            service_dict (dict): Request yolula gelen kayıtlar,
                    HizmetIHSDelete servisinin alanlarıyla eşlenmektedir.
                    Servis tarafında gerekli olan alanlar listede tutulmaktadır.

        """

        self.service_name = 'HizmetIHSDelete'

        self.service_dict['fields']['tckn'] = self.request.payload.get('tckn', '')
        self.service_dict['fields']['kayitNo'] = self.request.payload.get('kayit_no', '')
        self.service_dict['required_fields'] = ['tckn', 'kayitNo']

        super(HizmetIHSSil, self).handle()
