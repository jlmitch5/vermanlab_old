from tastypie.resources import ModelResource
from schema_kernel.models import KernelVersion, PCIModule, PCIAliases

class KernelVersionResource(ModelResource):
    class Meta:
        queryset = KernelVersion.objects.all()

class PCIModuleResource(ModelResource):
    class Meta:
        queryset = PCIModule.objects.all()

class PCIAliasesResource(ModelResource):
    class Meta:
        queryset = PCIAliases.objects.all()
