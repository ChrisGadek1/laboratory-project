# Generated by Django 3.1.7 on 2021-05-03 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0004_auto_20210503_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampling',
            name='collection_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='sampling',
            name='delivery_date',
            field=models.DateField(null=True),
        ),
    ]