# Generated by Django 3.1.7 on 2021-03-20 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0002_auto_20210320_0204'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControlType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MetodAndNorm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='sample',
            name='control_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='samples.controltype'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sampling_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='samples.metodandnorm'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='samples.type'),
        ),
    ]
