from django.db import models

class pciam(models.Model):
    val = models.CharField(max_length=19, unique=True)
    v = models.CharField(max_length=50, null=True, blank=True)
    d = models.CharField(max_length=50, null=True, blank=True)
    s = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.val)