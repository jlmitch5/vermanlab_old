import json

from collections import namedtuple

from django.http import Http404, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from schema_kernel.models import KernelVersion, PCIModule, PCIAliases
from schema_kernel.serializers import KernelVersionSerializer

# get all the kernel version in the system
class GetKernelVersions(APIView):
    def get(self, request, format=None):
        kvs = KernelVersion.objects.all()
        serializer = KernelVersionSerializer(kvs, many=True)
        return Response(serializer.data)

# get all diff information for the differences in modules/aliases for two kernel versions
class Diff(APIView):

    # remove aliases for analogous modules
    def get_and_remove_similar_aliases(self, mod_id_1, mod_id_2):
        pretty_aliases_kv_1 = []
        pretty_aliases_kv_2 = []

        Alias = namedtuple('Alias', 'vendor, device, subvendor, subdevice')

        aliases_kv_1 = {
            Alias(
                vendor=PCIAliases.vendor,
                device=PCIAliases.device,
                subvendor=PCIAliases.subvendor,
                subdevice=PCIAliases.subdevice
            ) for PCIAliases in PCIAliases.objects.filter(module=mod_id_1)
        }

        aliases_kv_2 = {
            Alias(
                vendor=PCIAliases.vendor,
                device=PCIAliases.device,
                subvendor=PCIAliases.subvendor,
                subdevice=PCIAliases.subdevice
            ) for PCIAliases in PCIAliases.objects.filter(module=mod_id_2)
        }

        return aliases_kv_1.difference(aliases_kv_2), aliases_kv_2.difference(aliases_kv_1)

    def pad_value(self, string_to_pad):
        if string_to_pad != 'null':
            s = '0000'
            s += string_to_pad
            return s[-4:]
        return "null"

    def chop_aliases(self, alias):
        s = ""
        a = self.pad_value(alias.vendor)
        if (a != "null"):
            s += a
        s += ":"
        a = self.pad_value(alias.device)
        if (a != "null"):
            s += a
        a = self.pad_value(alias.subvendor)
        if (a != "null"):
            s += ":"
            s += a
        a = self.pad_value(alias.subdevice)
        if (a != "null"):
            s += ":"
            s += a

        return s

    # remove modules from each list of mods that are the same
    def get_and_remove_same_modules(self, kv_1, kv_2):
        mods_all_kv_1 = {
            PCIModule.id for PCIModule in PCIModule.objects.filter(kernelVersionModuleConnector=kv_1)
        }
        mods_all_kv_2 = {
            PCIModule.id for PCIModule in PCIModule.objects.filter(kernelVersionModuleConnector=kv_2)
        }

        return PCIModule.objects.filter(
            id__in=list(
                mods_all_kv_1.difference(mods_all_kv_2)
            )
        ), PCIModule.objects.filter(
            id__in=list(
                mods_all_kv_2.difference(mods_all_kv_1)
            )
        )

    def get_kv(self, name):
        return KernelVersion.objects.get(name=name)

    def get(self, request, name1, name2, format=None):
        diff_vsn_val = 0
        old_mod_val = 0
        old_vsn_val = 0
        new_mod_val = 0
        new_vsn_val = 0

        # instantiate the mod pairslist
        mod_pairs_list = []

        # get the kernel version ids
        kv_obj_1 = self.get_kv(name1)
        kv_obj_2 = self.get_kv(name2)

        # get the lists of different modules
        kv_1_mods, kv_2_mods = self.get_and_remove_same_modules(kv_obj_1, kv_obj_2)
        kv_1_mod_names = {
            PCIModule.name for PCIModule in kv_1_mods
        }
        kv_2_mod_names = {
            PCIModule.name for PCIModule in kv_2_mods
        }

        all_mod_names = kv_1_mod_names.union(kv_2_mod_names)
        all_mod_names_sorted = sorted(all_mod_names)

        names_in_both_kvs = kv_1_mod_names.intersection(kv_2_mod_names)
        kv_1_mod_names = kv_1_mod_names.difference(names_in_both_kvs)
        kv_2_mod_names = kv_2_mod_names.difference(names_in_both_kvs)

        for mod_name in all_mod_names_sorted:
            if mod_name in kv_1_mod_names:
                alias_strings_serialized = []

                mod = PCIModule.objects.get(name=mod_name, kernelVersionModuleConnector=kv_obj_1)
                mod.version = mod.version.rstrip('\n')
                mod.srcversion = mod.srcversion.rstrip('\n')
                if mod.version is "NULL":
                    mod.version = None
                if mod.srcversion is "NULL":
                    mod.srcversion = None

                aliases = PCIAliases.objects.filter(module=mod)
                for alias in aliases:
                    alias_strings_serialized.append(self.chop_aliases(alias))

                mod_pairs_list.append( 
                    {
                        "kernel_one_module":
                        {
                            "kernel_version": name1,
                            "module_name": mod.name,
                            "version": mod.version,
                            "srcversion": mod.srcversion,
                            "aliases": alias_strings_serialized
                        },
                        "kernel_two_module": None
                    }
                )

                old_mod_val += 1
            elif mod_name in kv_2_mod_names:
                alias_strings_serialized = []

                mod = PCIModule.objects.get(name=mod_name, kernelVersionModuleConnector=kv_obj_2)
                mod.version = mod.version.rstrip('\n')
                mod.srcversion = mod.srcversion.rstrip('\n')
                if mod.version is "NULL":
                    mod.version = None
                if mod.srcversion is "NULL":
                    mod.srcversion = None

                aliases = PCIAliases.objects.filter(module=mod)
                for alias in aliases:
                    alias_strings_serialized.append(self.chop_aliases(alias))

                mod_pairs_list.append( 
                    {
                        "kernel_one_module": None,
                        "kernel_two_module":
                        {
                            "kernel_version": name2,
                            "module_name": mod.name,
                            "version": mod.version,
                            "srcversion": mod.srcversion,
                            "aliases": alias_strings_serialized
                        }
                    }
                )

                new_mod_val += 1
            else:
                alias_strings_1 = []
                alias_strings_2 = []
                mod_1 = PCIModule.objects.get(name=mod_name, kernelVersionModuleConnector=kv_obj_1)
                mod_2 = PCIModule.objects.get(name=mod_name, kernelVersionModuleConnector=kv_obj_2)
                mod_1.version = mod_1.version.rstrip('\n')
                mod_1.srcversion = mod_1.srcversion.rstrip('\n')

                #TODO NULL -> none doesn't work
                if mod_1.version is "NULL":
                    mod_1.version = None
                if mod_1.srcversion is "NULL":
                    mod_1.srcversion = None
                mod_2.version = mod_2.version.rstrip('\n')
                mod_2.srcversion = mod_2.srcversion.rstrip('\n')
                if mod_2.version is "NULL":
                    mod_2.version = None
                if mod_2.srcversion is "NULL":
                    mod_2.srcversion = None

                mod_1_aliases, mod_2_aliases = self.get_and_remove_similar_aliases(mod_1, mod_2)
                for alias in mod_1_aliases:
                    alias_strings_1.append(self.chop_aliases(alias))
                for alias in mod_2_aliases:
                    alias_strings_2.append(self.chop_aliases(alias))
                if not mod_1_aliases and not mod_2_aliases:
                    diff_vsn_val += 1
                else:
                    if mod_1_aliases:
                        old_vsn_val += 1
                    if mod_2_aliases:
                        new_vsn_val += 1

                mod_pairs_list.append( 
                    {
                        "kernel_one_module": {
                            "kernel_version": name1,
                            "module_name": mod_1.name,
                            "version": mod_1.version,
                            "srcversion": mod_1.srcversion,
                            "aliases": alias_strings_1
                        },
                        "kernel_two_module":
                        {
                            "kernel_version": name2,
                            "module_name": mod_2.name,
                            "version": mod_2.version,
                            "srcversion": mod_2.srcversion,
                            "aliases": alias_strings_2
                        }
                    }
                )

        mod_pairs_list_with_values = {
            "diff_vsn_val": diff_vsn_val,
            "old_vsn_val": old_vsn_val,
            "old_mod_val": old_mod_val,
            "new_vsn_val": new_vsn_val,
            "new_mod_val": new_mod_val,
            "mod_pairs_list": mod_pairs_list
        }

        return HttpResponse(json.dumps(mod_pairs_list_with_values), content_type="application/json")


