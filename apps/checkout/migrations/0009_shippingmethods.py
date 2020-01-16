# Generated by Django 2.2.6 on 2019-12-28 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_auto_20191108_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingMethods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('delivery_by_correios', 'Entrega via Correios'), ('store_pickup', 'Retirada na Loja'), ('fixed_price', 'Entrega com Preço Fixo')], default='delivery_by_correios', max_length=30, verbose_name='Opção de Entrega')),
            ],
        ),
    ]
