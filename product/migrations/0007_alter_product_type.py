# Generated by Django 5.0.2 on 2024-03-01 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_rename_mrp_product_discount_remove_product_delivered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('New_Arrivals', 'New_Arrivals'), ('Top_Rated', 'Top_Rated'), ('Featured', 'Featured')], max_length=25),
        ),
    ]
