# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import post,UserProfile

# Register your models here.

class postAdmin(admin.ModelAdmin):
    list_display=["title","published","author"]
    class Meta:
        model=post

class UserProfileModel(admin.ModelAdmin):
    list_display=["user","mobile"]
    class Meta:
        model=UserProfile

admin.site.register(post,postAdmin)
admin.site.register(UserProfile,UserProfileModel)
