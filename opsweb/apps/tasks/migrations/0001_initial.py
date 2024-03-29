# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-26 03:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0006_periodictask_priority'),
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='任务名称')),
                ('playbook', models.FileField(upload_to='playbook/%Y/%m', verbose_name='playbook文件')),
                ('detail_result', models.TextField(blank=True, null=True, verbose_name='执行结果详情')),
                ('status', models.CharField(choices=[('Y', '已执行'), ('N', '未执行')], default='N', max_length=1, verbose_name='执行状态')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='任务创建时间')),
                ('exec_time', models.DateTimeField(auto_now=True, verbose_name='执行时间')),
                ('user', models.CharField(help_text='执行用户', max_length=50, null=True, verbose_name='执行用户')),
            ],
            options={
                'verbose_name': '批量任务',
                'verbose_name_plural': '批量任务',
                'db_table': 'batchtask',
                'ordering': ['-add_time'],
                'permissions': (('view_batchTask', '查看批量任务'), ('add_batchTask', '添加批量任务'), ('change_batchTask', '修改批量任务'), ('delete_batchTask', '删除批量任务')),
            },
        ),
        migrations.CreateModel(
            name='TaskProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(help_text='执行用户', max_length=50, null=True, verbose_name='执行用户')),
                ('server', models.ForeignKey(help_text='服务器', null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Server', verbose_name='服务器')),
                ('task_profile', models.OneToOneField(help_text='PeriodicTask添加字段', on_delete=django.db.models.deletion.CASCADE, related_name='task_profile', to='django_celery_beat.PeriodicTask')),
            ],
            options={
                'verbose_name': '定时任务',
                'db_table': 'task_profile',
                'ordering': ['id'],
                'permissions': (('view_task', '查看定时任务'), ('add_task', '添加定时任务'), ('change_task', '修改定时任务'), ('delete_task', '删除定时任务')),
            },
        ),
    ]
