# Generated by Django 3.1.4 on 2021-03-13 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210313_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate_album',
            name='Like',
        ),
        migrations.RemoveField(
            model_name='rate_music',
            name='Like',
        ),
    ]
