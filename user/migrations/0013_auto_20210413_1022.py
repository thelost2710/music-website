# Generated by Django 3.1.4 on 2021-04-13 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_userinfotmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='Like',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='music',
            name='Like',
            field=models.IntegerField(default=0),
        ),
    ]
