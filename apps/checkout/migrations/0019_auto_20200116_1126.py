# Generated by Django 2.2.6 on 2020-01-16 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0018_auto_20200114_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_option',
        ),
        migrations.AddField(
            model_name='paymentmethods',
            name='order',
            field=models.ForeignKey(default=107, on_delete=django.db.models.deletion.CASCADE, related_name='payment_method', to='checkout.Order', verbose_name='Pedido'),
        ),
    ]
