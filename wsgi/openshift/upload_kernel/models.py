# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import settings

class Document(models.Model):
    docfile = models.FileField(upload_to='to_be_added')

    def pretty_name(self):
	no_path_name = self.docfile.name.split('/')[-1]
	return no_path_name[:-7]
