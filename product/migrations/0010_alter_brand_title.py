# Generated by Django 5.0.2 on 2024-03-13 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_category_title_alter_product_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
