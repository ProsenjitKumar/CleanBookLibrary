# Generated by Django 2.1.5 on 2019-01-22 10:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_remove_book_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2019, 1, 22, 10, 20, 56, 136177, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
