from django.contrib import admin
from schema_kernel.models import KernelVersion, PCIModule, PCIAliases

# Register your models here.
admin.site.register(KernelVersion)
admin.site.register(PCIModule)
admin.site.register(PCIAliases)
