# Generated by Django 3.2.6 on 2022-06-09 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20220609_0110'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritesPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.common')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
    ]
