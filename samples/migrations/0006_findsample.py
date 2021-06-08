# Generated by Django 3.1.7 on 2021-06-08 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0005_auto_20210608_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='FindSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='samples.sampling')),
            ],
        ),
    ]