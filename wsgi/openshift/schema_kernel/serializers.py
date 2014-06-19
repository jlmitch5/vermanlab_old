from rest_framework import serializers
from schema_kernel.models import KernelVersion, PCIModule, PCIAliases

class KernelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KernelVersion
        fields = ('name',)
