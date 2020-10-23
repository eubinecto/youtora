# Generated by Django 3.0.5 on 2020-10-22 04:47

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('refine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idiom',
            name='defs',
        ),
        migrations.AddField(
            model_name='idiom',
            name='def_sets',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.jsonb.JSONField(blank=True), blank=True, default=list,
                size=None),
        ),
    ]