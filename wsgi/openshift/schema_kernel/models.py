from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db import IntegrityError

# Kernel Version is the version of the kernel that contains specific modules
class KernelVersion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    pretty_kernel_version_name = models.CharField(max_length=100, default="kernel version")

    # returns the KernelVersion name
    def __unicode__(self):
        return unicode(self.name)

# Modules are referenced by the Kernel, and contain Aliases with which to relate their hardware support
class PCIModule(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=100, null=True, blank=True)
    srcversion = models.CharField(max_length=24, null=True, blank=True)
    # many-to-many constraint for kernel -> pci connection
    kernelVersionModuleConnector = models.ManyToManyField(KernelVersion)
    
    # the name, version, and srcversion must be a unique combination
    class Meta:
        unique_together = ('name', 'version', 'srcversion')

    # returns the Module name version and source version
    def __unicode__(self):
        moduleString = self.name
        if self.version != "NULL":
            moduleString += " "
            moduleString += self.version
        if self.srcversion != "NULL":
            moduleString += " "
            moduleString += self.srcversion
        return unicode(moduleString)

# the Kernel Version must not have two modules of the same name
@receiver(m2m_changed, sender=PCIModule.kernelVersionModuleConnector.through)
def verify_uniqueness(sender, **kwargs):
    module = kwargs.get('instance', None)
    action = kwargs.get('action', None)
    kernelVersions = kwargs.get('pk_set', None)

    if action == 'pre_add':
        for kernelVersion in kernelVersions:
            if PCIModule.objects.filter(name=module.name).filter(kernelVersionModuleConnector=kernelVersion):
                raise IntegrityError('PCIModule with name %s already exists for kernel version %s' % (module.name, KernelVersion.objects.get(pk=kernelVersion)))

# Aliases are referenced by specific modules, and relate hardware devices by vendor, device, subvendor, subdevice
class PCIAliases(models.Model):
    module = models.ManyToManyField(PCIModule)
    vendor = models.CharField(max_length=4)
    subvendor = models.CharField(max_length=4)
    device = models.CharField(max_length=4)
    subdevice = models.CharField(max_length=4)

    # these values must be hardcorded null in order for the unique_together constraint to pass
    class Meta:
        unique_together = ('vendor', 'subvendor', 'device', 'subdevice')

    # helper method for getRawAliasFromNamedTuple, returns a string of exactly 4 characters padded with 0
    def padAliasComponent(self, aliasComponentToPad):
        if aliasComponentToPad != 'null':
            aliasComponent = '0000'
            aliasComponent += aliasComponentToPad
            return aliasComponent[-4:]
        return "null"

    # method that takes an alias object from the DB and turns it into a colon-separated string
    def getRawAlias(self):
        # only return as many alias compoennts as exist
        rawAlias = ""
        aliasComponent = self.padAliasComponent(self.vendor)
        if (aliasComponent != "null"):
            rawAlias += aliasComponent
        aliasComponent = self.padAliasComponent(self.device)
        if (aliasComponent != "null"):
            rawAlias += ":"
            rawAlias += aliasComponent
        aliasComponent = self.padAliasComponent(self.subvendor)
        if (aliasComponent != "null"):
            rawAlias += ":"
            rawAlias += aliasComponent
        aliasComponent = self.padAliasComponent(self.subdevice)
        if (aliasComponent != "null"):
            rawAlias += ":"
            rawAlias += aliasComponent
        return rawAlias

    # returns the alias for the device
    def __unicode__(self):
        return unicode(self.getRawAlias())


