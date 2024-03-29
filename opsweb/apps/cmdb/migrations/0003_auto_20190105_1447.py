# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-01-05 06:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0002_auto_20190105_1442'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='env',
            options={'ordering': ['id'], 'permissions': (('view_env', '查看环境'),), 'verbose_name': '环境'},
        ),
        migrations.AlterModelOptions(
            name='idc',
            options={'ordering': ['id'], 'permissions': (('view_idc', '查看厂商'),), 'verbose_name': '厂商'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id'], 'permissions': (('view_product', '查看业务线'),), 'verbose_name': '业务'},
        ),
        migrations.AlterModelOptions(
            name='server',
            options={'ordering': ['id'], 'permissions': (('view_server', '查看服务器'),), 'verbose_name': '服务器'},
        ),
    ]
