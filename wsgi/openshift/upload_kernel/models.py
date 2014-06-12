# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Kernel_Tarball(models.Model):
    docfile = models.FileField(upload_to='to_be_added')

    def pretty_name(self):
	no_path_name = self.docfile.name.split('/')[-1]
	return no_path_name[:-7]

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Kernel_Tarball)
def kernel_tarball_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.docfile.delete(False)

class Shell_Script(models.Model):
    docfile = models.FileField(upload_to='scripts')

    def pretty_name(self):
	no_path_name = self.docfile.name.split('/')[-1]
	return no_path_name[:-3]
