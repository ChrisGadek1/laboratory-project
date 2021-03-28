from django.db import models
# Create your models here.

from datetime import date

#from app import forms


class WIJHARS(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name


class ControlType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name


class MetodAndNorm(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name


class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name


class DeliveryWay(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name


class ResearchStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name


class Sampling(models.Model):
    number = models.IntegerField()
    code = models.CharField(max_length=100)
    WIJHARS = models.ForeignKey(WIJHARS, on_delete=models.PROTECT,blank=False)
    assortment = models.TextField()
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
    manufacturer_name = models.CharField(max_length=300)
    manufacturer_address = models.CharField(max_length=500)
    sample_getter1_name = models.CharField(max_length=50)
    sample_getter1_surname = models.CharField(max_length=100) #dane osób pobierających próbki
    sample_getter1_position = models.CharField(max_length=100)
    sample_getter2_name = models.CharField(max_length=50)
    sample_getter2_surname = models.CharField(max_length=100)
    sample_getter2_position = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=300)
    final_consumer = models.BooleanField()
    consumer_name = models.CharField(max_length=100)
    consumer_address = models.CharField(max_length=200)
    order_number = models.IntegerField()
    mechanism_name_and_symbol = models.TextField()
    sample_delivery = models.ForeignKey(DeliveryWay, on_delete=models.PROTECT)


class Research(models.Model):
    sampling = models.ForeignKey(Sampling, on_delete=models.PROTECT)
    name = models.CharField(max_length=300)
    marking = models.CharField(max_length=300)
    nutritional_value = models.CharField(max_length=300)
    specification = models.CharField(max_length=300)
    ordinance = models.CharField(max_length=300)
    samples_number = models.IntegerField()
    result = models.IntegerField(max_length=300)
    start_date = models.DateField()
    completion_date = models.DateField()
    status = models.ForeignKey(ResearchStatus, on_delete=models.PROTECT)
    uncertainty = models.CharField(max_length=300)
    summary_meet_requirements = models.BooleanField()
    summary_requirements_explains = models.TextField()
