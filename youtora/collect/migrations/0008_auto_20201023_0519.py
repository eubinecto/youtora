# Generated by Django 3.0.5 on 2020-10-23 05:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('collect', '0007_auto_20201022_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracksraw',
            name='caption_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='tracksraw',
            name='raw_xml',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]