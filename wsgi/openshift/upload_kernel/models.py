# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Document(models.Model):
    docfile = models.FileField(upload_to='') #default location to upload: to_be_added

    @receiver(post_delete, sender=Document)
    def photo_post_delete_handler(sender, **kwargs):
        document = kwargs['instance']
        storage, path = document.storage, document.path
        storage.delete(path)