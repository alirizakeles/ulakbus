# -*-  coding: utf-8 -*-

from ulakbus.lib.role import AbsRole
from ulakbus.models.auth import AbstractRole

insert = 0

for abs_role in AbsRole:
    new_abs_role = AbstractRole()
    new_abs_role.name = str(abs_role.value)
    new_abs_role.id = abs_role.name
    new_abs_role.save()
    insert += 1

    print "%s eklendi"%abs_role.name

print "%i adet Soyut Rol Eklendi"%insert