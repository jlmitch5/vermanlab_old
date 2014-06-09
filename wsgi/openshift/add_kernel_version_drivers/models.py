from django.db import models

# Create your models here.

# Kernel Version is the version of the kernel that contains specific modules
class KernelVersion(models.Model):
    name = models.CharField(max_length=100)
    dateAdded = models.DateTimeField('date kernel version collected')

    # returns the KernelVersion name
    def __unicode__(self):
        return name


    # TODO: add delete functionality via checking
    # exclusivity of module relations
    # used for table-level KernelVersion functions
    # 1) checking exclusivity of module relation
    # objects = KernelVersionManager

# KernelVersionManager is used to see if the KernelVersion has
# exclusively related modules
# class KernelVersionManager(models.Manager)
    # TODO: write code to check for exclusivity

# Modules are referenced by the Kernel, and contain Aliases with which to relate their hardware support
class PCIModule(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    srcversion = models.CharField(max_length=100, null=True, blank=True)
    # we'll give this a many-to-many relationship with the Kernel Version
    # may be updated with the connector additions (tags) later
    kernelVersionModuleConnector = models.ManyToManyField('KernelVersion', through='KernelVersionModuleConnector')
    
    # is this okay, if it's not referencing a foreign key?
    # again, any of these values *can* be null
    class Meta:
        unique_together = ('name', 'version', 'srcversion')

    # returns the Module name version and source version
    def __unicode__(self):
        return self.name+" "+self.version+" "+self.srcversion

class KernelVersionModuleConnector(models.Model):
    module = models.ForeignKey(PCIModule)
    kernel = models.ForeignKey(KernelVersion)

# this is superfluous right now...may come in use with "tags"
# "tags" will also have to encapsulate alias data
# the kernel version and module are connected in this class
# class PCIKernelModuleConnector(models.Model):
#    kernel = models.ForeignKey(KernelVersion)
#    module = models.ForeignKey(PCIModule)
#
    # is this necessary, if it's referencing ALL keys
#    class Meta:
#        unique_together = ('kernel', 'module')

# Aliases are referenced by specific modules, and relate hardware devices by vendor, device, subvendor, subdevice
class PCIAliases(models.Model):
    module = models.ForeignKey(PCIModule)
    vendor = models.CharField(max_length=4, null=True, blank=True)
    subvendor = models.CharField(max_length=4, null=True, blank=True)
    device = models.CharField(max_length=4, null=True, blank=True)
    subdevice = models.CharField(max_length=4, null=True, blank=True)

    # check
    class Meta:
        unique_together = ('module', 'vendor', 'subvendor', 'device', 'subdevice')

    # returns the alias for the device
    def __unicode__(self):
        return self.module+": "+self.vendor+":"+self.device+":"+self.subvendor+":"+self.subdevice
