# Generated by Django 2.2.6 on 2019-10-27 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0002_auto_20191027_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_key', models.CharField(db_index=True, max_length=40, verbose_name='Chave do Carrinho')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantidade')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preço')),
                ('product', models.ForeignKey(on_delete='SET_NULL', to='catalog.Product', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Item do Carrinho',
                'verbose_name_plural': 'Itens dos Carrinhos',
            },
        ),
    ]
