# Generated by Django 2.2.6 on 2019-11-08 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Image',
            new_name='image',
        ),
    ]
