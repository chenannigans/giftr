from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Gift(models.Model):
	user = models.ForeignKey(User)
	picture = models.CharField(max_length=100)
	photo = models.ImageField(upload_to="gifts-photos", blank=True)
	description = models.CharField(max_length=100, null=False)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)
	url = models.CharField(max_length=200)
	# gift_category = models.ManyToManyField(GiftCategory)
	# recipient_category = models.ManyToManyField(RecipientCatetory)
	category = models.CharField(max_length=200)
	recipient_category = models.CharField(max_length=200)

class RecipientCatetory(models.Model):
	name = models.CharField(max_length=100)

class GiftCategory(models.Model):
	categoryName = models.CharField(max_length=100)
