# Generated by Django 3.2.9 on 2021-12-27 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0006_auto_20211227_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='size'),
        ),
    ]