# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import settings

class Document(models.Model):
    docfile = models.FileField(upload_to=(settings.MEDIA_ROOT)) #default location to upload: to_be_added
