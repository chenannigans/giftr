from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Posts(models.Model):
    text = models.CharField(max_length = 42)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['timestamp']
    def __unicode__(self):
            return self.text

class Profile(models.Model):
    user = models.ForeignKey(User)
    bio = models.CharField(max_length = 420)
    age = models.CharField(max_length = 2)
    picture = models.ImageField(upload_to="photos",blank=True)
    def __unicode__(self):
            return self.user

class Follow(models.Model):
    user = models.ForeignKey(User)
    following = models.ManyToManyField(User, related_name='following_users')
    def __unicode__(self):
            return self.user
