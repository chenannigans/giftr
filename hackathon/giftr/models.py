from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Gift(models.Model):
	user = models.ForeignKey(User)
	picture = models.FileField(upload_to=user_directory_path)
	description = models.CharField(max_length=100)
	price = models.DateTimeField(max_digits=None, decimal_places = 2)
	url = models.CharField(max_length=None)
	category = models.CharField(max_length=None)
	recipient_category = models.CharField(max_length=None)

