# Generated by Django 5.1.5 on 2025-03-21 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='available_at_store',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='order_quantity',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(choices=[('qty', 'Số lượng'), ('container', 'Container')], default='qty', max_length=20),
        ),
    ]
