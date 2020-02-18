from django.contrib.auth.models import User
from django.db import models
from model_utils import Choices


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    TYPE = Choices(('fundacja', ('fundacja')), ('organizacja pozarządowa', ('organizacja pozarządowa')), ('zbiórka lokalna', ('zbiórka lokalna')))
    type = models.CharField(max_length=25, choices=TYPE, default=TYPE.fundacja)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, models.SET_NULL, null=True)
    address = models.CharField(max_length=64)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, models.SET_NULL, null=True)


