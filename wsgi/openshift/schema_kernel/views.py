from schema_kernel.models import KernelVersion, PCIModule, PCIAliases
from schema_kernel.serializers import KernelVersionSerializer, KernelVersionIDSerializer, PCIModuleSerializer, PCIModuleIDSerializer, PCIModuleInfoSerializer, AliasDiffSerializer, AliasByModSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from itertools import chain

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

class PCIMList(APIView):
    def get(self, request, format=None):
        mods = PCIModule.objects.all()
        serializer = PCIModuleSerializer(mods, many=True)
        return Response(serializer.data)

class PCIMList_by_kv(APIView):
    def get_object(self, name):
        try:
            return KernelVersion.objects.get(name=name)
        except KernelVersion.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        kv = self.get_object(name)
        mods = PCIModule.objects.filter(kernelVersionModuleConnector=kv).order_by('name')
        serializer = PCIModuleSerializer(mods, many=True)
        return Response(serializer.data)

class PCIMList_intersection(APIView):
    def get_object(self, name):
        try:
            return KernelVersion.objects.get(name=name)
        except KernelVersion.DoesNotExist:
            raise Http404
    
    def get(self, request, name1, name2, format=None):
        kv1 = self.get_object(name1)
        kv2 = self.get_object(name2)
        mods = PCIModule.objects.filter(kernelVersionModuleConnector=kv1).exclude(kernelVersionModuleConnector=kv2) | PCIModule.objects.filter(kernelVersionModuleConnector=kv2).exclude(kernelVersionModuleConnector=kv1)
        mods = mods.order_by("name")
        serializer = PCIModuleSerializer(mods, many=True)
        return Response(serializer.data)

class KVID(APIView):
    def get_object(self, name):
        try:
            return KernelVersion.objects.get(name=name)
        except KernelVersion.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        kv = self.get_object(name)
        serializer = KernelVersionIDSerializer(kv)
        return Response(serializer.data)

class ModID(APIView):
    def get_object(self, name, version, srcversion):
        try:
            return PCIModule.objects.get(name=name, version=version, srcversion=srcversion)
        except PCIModule.DoesNotExist:
            raise Http404

    def get(self, request, name, version, srcversion, format=None):
        mod = self.get_object(name, version, srcversion)
        serializer = KernelVersionIDSerializer(mod)
        return Response(serializer.data)

class ModPretty(APIView):
    def get_object(self, id):
        try:
            return PCIModule.objects.get(id=id)
        except PCIModule.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        mod = self.get_object(id)
        serializer = PCIModuleInfoSerializer(mod)
        return Response(serializer.data)

class AliasDiff(APIView):
    def get_object(self, mod_id):
        try:
            return PCIModule.objects.get(id=mod_id)
        except PCIModule.DoesNotExist:
            raise Http404

    def get(self, request, mod_id_1, mod_id_2, format=None):
        mod1 = self.get_object(mod_id_1)
        mod2 = self.get_object(mod_id_2)
        aliases = PCIAliases.objects.filter(module=mod_id_1)
        aliases2 = PCIAliases.objects.filter(module=mod_id_2)
        # for alias in aliases:
        #     vendor = (alias.vendor)
        #     device = (alias.device)
        #     subvendor = (alias.subvendor)
        #     subdevice = (alias.subdevice)
        #     aliases = aliases.exclude(vendor=vendor, device=device, subvendor=subvendor, subdevice=subdevice)
        #     aliases2 = aliases2.exclude(vendor=vendor, device=device, subvendor=subvendor, subdevice=subdevice)
        # for alias in aliases2:
        #     vendor = (alias.vendor)
        #     device = (alias.device)
        #     subvendor = (alias.subvendor)
        #     subdevice = (alias.subdevice)
        #     aliases = aliases.exclude(vendor=vendor, device=device, subvendor=subvendor, subdevice=subdevice)
        #     aliases2 = aliases2.exclude(vendor=vendor, device=device, subvendor=subvendor, subdevice=subdevice)
        aliases = aliases | aliases2
        if aliases:
            print True
        serializer = AliasDiffSerializer(aliases)
        return Response(serializer.data)

class AliasByMod(APIView):
    def get_object(self, module):
        try:
            return PCIModule.objects.get(id=module)
        except PCIModule.DoesNotExist:
            raise Http404

    def get(self, request, module, format=None):
        mod = self.get_object(module)
        aliases = PCIAliases.objects.filter(module=module)
        serializer = AliasByModSerializer(aliases)
        return Response(serializer.data)

