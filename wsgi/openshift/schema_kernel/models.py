from django.db import models
import datetime

# BEGIN Database schema

# Kernel Version is the version of the kernel that contains specific modules
class KernelVersion(models.Model):
    name = models.CharField(max_length=100, unique=True)
#    dateAdded = models.DateTimeField('date kernel version collected', default=datetime.datetime.now)

    # returns the KernelVersion name
    def __unicode__(self):
        return self.name

    # TODO: add delete functionality via checking exclusivity of module relations used for table-level KernelVersion functions

# TODO: Add KernelVersionManager (used to see if the KernelVersion has exclusively related modules)
# class KernelVersionManager(models.Manager):

# Modules are referenced by the Kernel, and contain Aliases with which to relate their hardware support
class PCIModule(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    srcversion = models.CharField(max_length=100, null=True, blank=True)
    # many-to-many constraint for kernel -> pci connection
    kernelVersionModuleConnector = models.ManyToManyField(KernelVersion)
    
    # TODO: check to see if okay, any of these values *can* be null
    class Meta:
        unique_together = ('name', 'version', 'srcversion')

    # returns the Module name version and source version
    def __unicode__(self):
        return self.name+" "+self.version+" "+self.srcversion

# Aliases are referenced by specific modules, and relate hardware devices by vendor, device, subvendor, subdevice
class PCIAliases(models.Model):
    module = models.ForeignKey(PCIModule)
    vendor = models.CharField(max_length=4, null=True, blank=True)
    subvendor = models.CharField(max_length=4, null=True, blank=True)
    device = models.CharField(max_length=4, null=True, blank=True)
    subdevice = models.CharField(max_length=4, null=True, blank=True)

    # TODO: check to see if okay, any of these values (aside from module) *can* be null
    class Meta:
        unique_together = ('module', 'vendor', 'subvendor', 'device', 'subdevice')

    # returns the alias for the device
    def __unicode__(self):
        return self.module.name+": "+self.vendor+":"+self.device+":"+self.subvendor+":"+self.subdevice

# TODO: Add a model that relates Module, Kernel and Alias for capability tagging
