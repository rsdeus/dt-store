# Generated by Django 2.2.6 on 2019-11-14 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20191114_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(blank=True, max_length=255, verbose_name='Descrição'),
        ),
    ]
