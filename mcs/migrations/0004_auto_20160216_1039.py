# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcs', '0003_auto_20160214_1310'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SMS',
            new_name='UnstructuredTXT',
        ),
    ]
