# Generated by Django 3.0.5 on 2020-10-22 07:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('refine', '0002_auto_20201022_0447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idiom',
            old_name='def_sets',
            new_name='meanings',
        ),
    ]
