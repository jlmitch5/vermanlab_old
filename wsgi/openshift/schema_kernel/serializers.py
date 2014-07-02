from rest_framework import serializers

from schema_kernel.models import KernelVersion, PCIModule

# the kernel version
class KernelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KernelVersion
        fields = ('name',)

# the module
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCIModule
        fields = ('name', 'version', 'srcversion',)

# TODO: change schema of serializer to just one field
# the serializer for the aliases of a module
class AliasSerializer(serializers.Serializer):
    serializers.CharField(max_length=19)

# START DIFF SERIALIZERS
# the serializer for a module in the diff tree
class DiffModuleSerializer(serializers.Serializer):
    kernelVersion = KernelVersionSerializer()
    module = ModuleSerializer()
    aliases = AliasSerializer(many=True, required=False)

# the serializer for a pair of KernelVersionModules
class ModulePairSerializer(serializers.Serializer):
    kernelOneModule = DiffModuleSerializer(required=False)
    kernelTwoModule = DiffModuleSerializer(required=False)

# the serializer for all the pairs of modules in two kernels
class ModulePairListSerializer(serializers.Serializer):
    ModulePairSerializer(many=True)