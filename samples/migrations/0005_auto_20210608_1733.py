# Generated by Django 3.1.7 on 2021-06-08 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0004_research_requirementstype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='findresearch',
            name='research_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='samples.research'),
        ),
    ]