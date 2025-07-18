# Generated by Django 5.2.3 on 2025-07-17 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_productsale_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsale',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.product'),
        ),
        migrations.AlterField(
            model_name='productsale',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_sales', to='project.sale'),
        ),
    ]
