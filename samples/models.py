from django.db import models
# Create your models here.

from datetime import date

#from app import forms


class WIJHARS(models.Model):
    name = models.CharField(max_length=100)


class ControlType(models.Model):
    name = models.CharField(max_length=100)


class MetodAndNorm(models.Model):
    name = models.CharField(max_length=100)


class Type(models.Model):
    name = models.CharField(max_length=100)


class Sample(models.Model):
    number = models.IntegerField()
    code = models.CharField(max_length=100)
    WIJHARS = models.ForeignKey(WIJHARS, on_delete=models.PROTECT,blank=False)
    assortment = models.CharField(max_length=100)
    admission_date = models.DateField(default=date.today)
    expiration_date = models.DateField()
    completion_date = models.DateField()
    additional_comment = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    condition = models.CharField(max_length=100,default = "Bez zastrzeżeń")
    appeal_analysis = models.BooleanField(default=False)
    control_type = models.ForeignKey(ControlType, on_delete=models.PROTECT)
    sampling_method = models.ForeignKey(MetodAndNorm, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
