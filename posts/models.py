# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField
from validator import FileValidator
# Create your models here.


validate_file = FileValidator(max_size=10* 1024 * 100)

class post(models.Model):
    title=models.CharField(max_length=150)
    description=HTMLField()
    featured_image=models.FileField(upload_to="images",blank=True, validators=[validate_file])
    published=models.DateTimeField(auto_now=False,auto_now_add=True)
    author = models.ForeignKey(User)


    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=12)
    image=models.ImageField(upload_to="images",default="images/img_avatar.png",blank=True)
    bio=models.TextField()


    def __unicode__(self):
        return unicode(self.user)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
