# Generated by Django 2.2.6 on 2019-10-30 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20191027_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete='CASCADE', to='catalog.Category', verbose_name='Categoria'),
        ),
    ]
