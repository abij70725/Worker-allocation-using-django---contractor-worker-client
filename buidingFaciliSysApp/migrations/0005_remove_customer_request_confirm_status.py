# Generated by Django 5.1.3 on 2025-01-24 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buidingFaciliSysApp', '0004_worker_proof'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer_request',
            name='confirm_status',
        ),
    ]
