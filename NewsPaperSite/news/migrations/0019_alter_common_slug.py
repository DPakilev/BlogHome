# Generated by Django 3.2.6 on 2022-06-13 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0018_alter_common_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='common',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]