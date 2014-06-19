from schema_kernel.models import KernelVersion
from schema_kernel.serializers import KernelVersionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class KVList(APIView):
    def get(self, request, format=None):
        kvs = KernelVersion.objects.all()
        serializer = KernelVersionSerializer(kvs, many=True)
        return Response(serializer.data)

class KVDetail(APIView):
    def get_object(self, name):
        try:
            return KernelVersion.objects.get(name=name)
        except KernelVersion.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        kv = self.get_object(name)
        serializer = KernelVersionSerializer(kv)
        return Response(serializer.data)

