# Generated by Django 2.2.6 on 2020-01-05 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20191115_0630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='bar_code',
        ),
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Código do Produto'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Peso'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Preço'),
        ),
    ]