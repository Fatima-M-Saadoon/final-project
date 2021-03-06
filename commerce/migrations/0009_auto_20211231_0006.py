# Generated by Django 3.2.9 on 2021-12-30 21:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commerce', '0008_alter_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commerce.product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='item',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
