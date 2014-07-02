from rest_framework import serializers
from schema_kernel.models import KernelVersion

class KernelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KernelVersion
        fields = ('name',)