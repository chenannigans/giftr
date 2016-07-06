from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Gift(models.Model):
	user = models.ForeignKey(User)
	picture = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=10, decimal_places = 2)
	url = models.CharField(max_length=200)
	category = models.CharField(max_length=200)
	recipient_category = models.CharField(max_length=200)


