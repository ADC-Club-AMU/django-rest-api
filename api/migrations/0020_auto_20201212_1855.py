# Generated by Django 3.1.4 on 2020-12-12 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20201212_1855'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entranceexamination',
            options={'ordering': ['day', 'month']},
        ),
    ]
