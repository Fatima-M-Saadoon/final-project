# Generated by Django 3.2.9 on 2021-12-30 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commerce', '0005_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='note',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ref_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.RemoveField(
            model_name='product',
            name='height',
        ),
        migrations.RemoveField(
            model_name='product',
            name='label',
        ),
        migrations.RemoveField(
            model_name='product',
            name='length',
        ),
        migrations.RemoveField(
            model_name='product',
            name='merchant',
        ),
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
        migrations.RemoveField(
            model_name='product',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='product',
            name='width',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='size'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='commerce.category', verbose_name='parent'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='commerce.category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cost',
            field=models.FloatField(verbose_name='cost'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.FloatField(default=0, verbose_name='discounted price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='qty',
            field=models.IntegerField(verbose_name='qty'),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Label',
        ),
        migrations.DeleteModel(
            name='Merchant',
        ),
        migrations.DeleteModel(
            name='OrderStatus',
        ),
        migrations.DeleteModel(
            name='Vendor',
        ),
    ]