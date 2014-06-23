from rest_framework import serializers
from schema_kernel.models import KernelVersion, PCIModule, PCIAliases

class KernelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KernelVersion
        fields = ('name',)

class KernelVersionIDSerializer(serializers.ModelSerializer):
	class Meta:
		model = KernelVersion
		fields = ('id',)

class PCIModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCIModule
        fields = ('id', 'name', 'kernelVersionModuleConnector')

class PCIModuleIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCIModule
        fields = ('id',)

class PCIModuleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCIModule
        fields = ('name', 'version', 'srcversion',)
