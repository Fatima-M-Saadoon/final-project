# Generated by Django 3.2.9 on 2021-12-30 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0006_auto_20211230_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='commerce.product', verbose_name='product'),
        ),
    ]
