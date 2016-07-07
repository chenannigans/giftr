from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class RecipientCatetory(models.Model):
	name = models.CharField(max_length=100)

class GiftCategory(models.Model):
	categoryName = models.CharField(max_length=100)


class Gift(models.Model):
	user = models.ForeignKey(User)
	photo = models.ImageField(upload_to="gifts-photos", default='gifts-photos/default-gift.jpg')
	description = models.CharField(max_length=100, null=False)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)
	url = models.CharField(max_length=200, blank=True, null=True)
	category = models.CharField(max_length=200, blank=True, null=True)
	recipient_category = models.CharField(max_length=200, blank=True, null=True)

