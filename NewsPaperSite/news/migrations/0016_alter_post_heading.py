# Generated by Django 3.2.6 on 2022-06-12 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_auto_20220611_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='heading',
            field=models.CharField(max_length=250),
        ),
    ]
