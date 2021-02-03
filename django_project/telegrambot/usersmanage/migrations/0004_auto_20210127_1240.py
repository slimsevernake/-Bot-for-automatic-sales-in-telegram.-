# Generated by Django 3.1.5 on 2021-01-27 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0003_goods_photo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='failedpurchase',
            name='amount_cost',
            field=models.DecimalField(decimal_places=2, default=2.0, max_digits=8, verbose_name='Сума'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='successfulpurchase',
            name='amount_cost',
            field=models.DecimalField(decimal_places=2, default=2.0, max_digits=8, verbose_name='Сума'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='address',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='city',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='city',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='failedpurchase',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='failedpurchase',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersmanage.goods', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='failedpurchase',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='goodsandaddress',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='goodsandaddress',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='successfulpurchase',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='successfulpurchase',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersmanage.goods', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='successfulpurchase',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
    ]