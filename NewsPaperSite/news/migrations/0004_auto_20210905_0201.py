# Generated by Django 3.2.6 on 2021-09-04 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_common'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='article_or_news',
        ),
    ]
