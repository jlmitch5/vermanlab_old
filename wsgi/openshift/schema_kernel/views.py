import json

from collections import namedtuple

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from schema_kernel.models import KernelVersion, PCIModule, PCIAliases
from pci_ids.models import pciam

from schema_kernel.serializers import KernelVersionSerializer

# get all the kernel version in the system
class GetKernelVersions(APIView):
    def get(self, request, format=None):
        kernelVersions = KernelVersion.objects.all()
        serializer = KernelVersionSerializer(kernelVersions, many=True)
        return Response(serializer.data)

# get all diff information for the differences in modules/aliases for two kernel versions
class Diff(APIView):
    # constants for the LHS (1) and RHS (2) kernels
    KERNEL_VERSION_1 = 1
    KERNEL_VERSION_2 = 2

    # get the readable device name from the pci_ids table by passing a raw alias value
    def getReadableDeviceNameFromAlias(self, alias):
        readableDeviceString = ""
        # this is a generic vendor used for non-consumer-facing devices by some companies.
        # it has no diagnostic value
        if alias[:4] == "1234":
            return None
        else:
            # try to get the readable alias, removing components until you have found an associated human readable device name
            # if you can't just return none
            try:
                readableDevice = pciam.objects.get(val__iexact=alias)
            except pciam.DoesNotExist:
                if len(alias) == 19 or len(alias) == 14:
                    try:
                        alias = alias[:9]
                        readableDevice = pciam.objects.get(val__iexact=alias)
                    except pciam.DoesNotExist:
                        try:
                            alias = alias[:4]
                            readableDevice = pciam.objects.get(val__iexact=alias)
                        except:
                            return None
                elif len(alias) == 9:
                    try:
                        alias = alias[:4]
                        readableDevice = pciam.objects.get(val__iexact=alias)
                    except:
                        return None
            if readableDevice.v:
                readableDeviceString += readableDevice.v
            if readableDevice.d:
                readableDeviceString += " "
                readableDeviceString += readableDevice.d
            if readableDevice.s:
                readableDeviceString += " "
                readableDeviceString += readableDevice.s
            return readableDeviceString

    # remove aliases for analogous modules
    def removeAnalogousAliases(self, module1, module2):
        # create a list of namedtuples (aliases), and return the ones that are different for each module version
        Alias = namedtuple('Alias', 'vendor, device, subvendor, subdevice')
        aliasesForModule1 = {Alias(vendor=PCIAliases.vendor, device=PCIAliases.device, subvendor=PCIAliases.subvendor, subdevice=PCIAliases.subdevice) for PCIAliases in PCIAliases.objects.filter(module=module1)}
        aliasesForModule2 = {Alias(vendor=PCIAliases.vendor, device=PCIAliases.device, subvendor=PCIAliases.subvendor, subdevice=PCIAliases.subdevice) for PCIAliases in PCIAliases.objects.filter(module=module2)}
        return aliasesForModule1.difference(aliasesForModule2), aliasesForModule2.difference(aliasesForModule1)

    # helper method for getRawAliasFromNamedTuple, returns a string of exactly 4 characters padded with 0
    def padAliasComponent(self, aliasComponentToPad):
        if aliasComponentToPad:
            aliasComponent = '0000'
            aliasComponent += aliasComponentToPad
            return aliasComponent[-4:]

    # method that takes an alias object from the DB and turns it into a colon-separated string
    def getRawAliasFromNamedTuple(self, alias):
        # only return as many alias components as exist
        rawAlias = ""
        if alias.vendor:
            rawAlias += self.padAliasComponent(alias.vendor)
        if alias.device:
            rawAlias += ":"
            rawAlias += self.padAliasComponent(alias.device)
        if alias.subvendor:
            rawAlias += ":"
            rawAlias += self.padAliasComponent(alias.subvendor)
        if alias.subdevice:
            rawAlias += ":"
            rawAlias += self.padAliasComponent(alias.subdevice)
        return rawAlias

    # get the aliases for a PCIModule
    def getAliasesForModule(self, module):
        aliases_to_return = []
        # create a list of namedtuples (aliases), and return the ones that are different for each module version
        Alias = namedtuple('Alias', 'vendor, device, subvendor, subdevice')
        aliases = {Alias(vendor=PCIAliases.vendor, device=PCIAliases.device, subvendor=PCIAliases.subvendor, subdevice=PCIAliases.subdevice) for PCIAliases in PCIAliases.objects.filter(module=module)}
        return self.serializeAliases(aliases)

    # get the raw alias (and the human readable device name) and serialize the aliases for the larger diff json structure
    def serializeAliases(self, aliases):
        aliasesSerialized = []
        for alias in aliases:
            rawAlias = self.getRawAliasFromNamedTuple(alias)
            humanReadableDeviceName = self.getReadableDeviceNameFromAlias(rawAlias)
            aliasesSerialized.append(
                {
                    "a":
                    {
                        "r": rawAlias,
                        "p": humanReadableDeviceName
                    }
                }
            )
        return aliasesSerialized

    # remove modules from each list of mods that are the same
    def removeAnalogousModules(self, kernelVersion1, kernelVersion2):
        # create the sets of all PCIModules related to one of the kernel versions
        modsInKernelVersion1 = {
            PCIModule.id for PCIModule in PCIModule.objects.filter(kernelVersionModuleConnector=kernelVersion1)
        }
        modsInKernelVersion2 = {
            PCIModule.id for PCIModule in PCIModule.objects.filter(kernelVersionModuleConnector=kernelVersion2)
        }

        # return the sets of PCIModules that only show up in one of the kernel versions
        return PCIModule.objects.filter(
            id__in=list(
                modsInKernelVersion1.difference(modsInKernelVersion2)
            )
        ), PCIModule.objects.filter(
            id__in=list(
                modsInKernelVersion2.difference(modsInKernelVersion1)
            )
        )

    # get the kernel version db object from the name
    def getKernelVersionObject(self, name):
        return KernelVersion.objects.get(name=name)

    # used to get a sorted version of all the module names, and list of the module names that are in each (or both) of the kernel versions
    def sortModulesAndPlaceInModuleCategories(self, kernelVersion1Modules, kernelVersion2Modules):
        # create sets out of the module names for each kernel version
        moduleNamesInKernelVersion1 = {
            PCIModule.name for PCIModule in kernelVersion1Modules
        }
        moduleNamesInKernelVersion2 = {
            PCIModule.name for PCIModule in kernelVersion2Modules
        }

        # sort all of the modules that will be returned (used to keep the rows in ABC order)
        sortedModuleNames = sorted(moduleNamesInKernelVersion1.union(moduleNamesInKernelVersion2))

        # get the list of modules in both kvs, or just one of the kvs
        modulesInBothKernelVersions = moduleNamesInKernelVersion1.intersection(moduleNamesInKernelVersion2)
        modulesOnlyInKernelVersion1 = moduleNamesInKernelVersion1.difference(modulesInBothKernelVersions)
        modulesOnlyInKernelVersion2 = moduleNamesInKernelVersion2.difference(modulesInBothKernelVersions)

        return sortedModuleNames, modulesInBothKernelVersions, modulesOnlyInKernelVersion1, modulesOnlyInKernelVersion2

    # get all the necessarily module pieces for serialization
    def getModuleObject(self, module, kernelObject):
        module = PCIModule.objects.get(name=module, kernelVersionModuleConnector=kernelObject)
        module.version = module.version.rstrip('\n')
        module.srcversion = module.srcversion.rstrip('\n')

        if module.version == "NULL":
            module.version = None
        if module.srcversion == "NULL":
            module.srcversion = None

        return module

    # serialize a single module, which will be appended to analogousModulePairList
    def serializeModule(self, selectedKernelVersion, kernelVersionName, module, aliases):
        if selectedKernelVersion == self.KERNEL_VERSION_1:
            return {
                "k1m": {
                    "kv": kernelVersionName,
                    "m": module.name,
                    "v": module.version,
                    "srcv": module.srcversion,
                    "a": aliases
                }
            }
        elif selectedKernelVersion == self.KERNEL_VERSION_2:
            return {
                "k2m": {
                    "kv": kernelVersionName,
                    "m": module.name,
                    "v": module.version,
                    "srcv": module.srcversion,
                    "a": aliases
                }
            }

    # calls the above methods to create the diff data structure and returns the JSON response
    def get(self, request, name1, name2, format=None):
        # the following values are used as the quantifiers for the types of datas returned in the diff tool:
        # this represents modules that are present in both kernels but have different versions or srcversions
        moduleHasDifferentVersions = 0
        # this represents a device present in the "old" (or left-hand side) kernel but not in the "new" (or RHS).  This is reserved for modules that only exist in the old kernel version
        moduleOnlyPresentInKernelVersion1Devices = 0
        # this represents a device present in the "old" (or left-hand side) kernel but not in the "new" (or RHS).  This is reserved for modules that exist (but in different versions/srcversions) in both kernel versions
        moduleVersionOnlyPresentInKernelVersion1Devices = 0
        # this represents a device present in the "new" (or right-hand side) kernel but not in the "old" (or LHS).  This is reserved for modules that only exist in the new kernel version
        moduleOnlyPresentInKernelVersion2Devices = 0
        # this represents a device present in the "new" (or right-hand side) kernel but not in the "old" (or LHS).  This is reserved for modules that exist (but in different versions/srcversions) in both kernel versions
        moduleVersionOnlyPresentInKernelVersion2Devices = 0

        # This list maps directly to the "rows" in the front end.  Each mod pair contains analagous modules (if present) and their relevant aliases/human-readable device names (if present)
        analogousModulePairList = []

        # This grabs the model objects from the give kernel name for both kernels
        kernelVersionObject1 = self.getKernelVersionObject(name1)
        kernelVersionObject2 = self.getKernelVersionObject(name2)

        # This gets the modules for each kernel and then returns the modules that are only present in either version (ie: deleting duplicates)
        kernelVersion1Modules, kernelVersion2Modules = self.removeAnalogousModules(kernelVersionObject1, kernelVersionObject2)

        # This returns a list of all the module names in alphabetical order, as well as lists of where these modules are located (in both kernels, or just in kernel 1 or kernel 2)
        sortedModuleNames, modulesInBothKernelVersions, modulesOnlyInKernelVersion1, modulesOnlyInKernelVersion2 = self.sortModulesAndPlaceInModuleCategories(kernelVersion1Modules, kernelVersion2Modules)

        # Iterate through every module
        for mod in sortedModuleNames:
            selectedKernelName = ""
            selectedKernelVersion = 0
            aliases = []
            # mod is only present in KernelVersion1
            if mod in modulesOnlyInKernelVersion1:
                # set the kernel version and name to KernelVersion1
                selectedKernelVersion = self.KERNEL_VERSION_1
                selectedKernelName = name1
                # set mod equal to the module object instead of the module name
                mod = self.getModuleObject(mod, kernelVersionObject1)
                # grab the aliases for this module
                aliases = self.getAliasesForModule(mod)
                # if they exist, increment the module device counter
                if aliases:
                    moduleOnlyPresentInKernelVersion1Devices += len(aliases)
                # append the value to the module pairlist
                analogousModulePairList.append(
                    {
                        'k1m' : self.serializeModule(selectedKernelVersion, selectedKernelName, mod, aliases)['k1m'],
                        'k2m' : None
                    }
                )
            # mod is only present in KernelVersion2
            elif mod in modulesOnlyInKernelVersion2:
                # set the kernel version and name to KernelVersion2
                selectedKernelVersion = self.KERNEL_VERSION_2
                selectedKernelName = name2
                # set mod equal to the module object instead of the module name
                mod = self.getModuleObject(mod, kernelVersionObject2)
                # grab the aliases for this module, and returns the serialized raw values and human-readable device names in an array
                aliases = self.getAliasesForModule(mod)
                # if they exist, increment the module device counter
                if aliases:
                    moduleOnlyPresentInKernelVersion2Devices += len(aliases)
                # append the value to the module pairlist
                analogousModulePairList.append(
                    {
                        'k2m' : self.serializeModule(selectedKernelVersion, selectedKernelName, mod, aliases)['k2m'],
                        'k1m' : None
                    }
                )
            elif mod in modulesInBothKernelVersions:
                # this module name is in both kernels with different versions...increment the counter
                moduleHasDifferentVersions += 1
                # get both of the analogous modules
                module1 = self.getModuleObject(mod, kernelVersionObject1)
                module2 = self.getModuleObject(mod, kernelVersionObject2)
                # this gets the aliases for each module and then returns the aliases that are only present in either version (ie: deleting duplicates)
                aliasesForModule1, aliasesForModule2 = self.removeAnalogousAliases(module1, module2)
                # serialize the aliases (get raw alias and human-readable device name)
                aliasesForModule1 = self.serializeAliases(aliasesForModule1)
                aliasesForModule2 = self.serializeAliases(aliasesForModule2)

                # increment the counters if the modules returned aliases
                if aliasesForModule1:
                    moduleVersionOnlyPresentInKernelVersion1Devices += len(aliasesForModule1)
                if aliasesForModule2:
                    moduleVersionOnlyPresentInKernelVersion2Devices += len(aliasesForModule2)
                # append the value to the module pairlist
                analogousModulePairList.append(
                    {
                        'k1m' : self.serializeModule(self.KERNEL_VERSION_1, name1, module1, aliasesForModule1)['k1m'],
                        'k2m' : self.serializeModule(self.KERNEL_VERSION_2, name2, module1, aliasesForModule2)['k2m']
                    }
                )
            
        # create the final data structure to be sent via JSON
        analogousModulePairListWithDiagnosticValues = {
            "dv": moduleHasDifferentVersions,
            "kv1v": moduleVersionOnlyPresentInKernelVersion1Devices,
            "kv1m": moduleOnlyPresentInKernelVersion1Devices,
            "kv2v": moduleVersionOnlyPresentInKernelVersion2Devices,
            "kv2m": moduleOnlyPresentInKernelVersion2Devices,
            "mods": analogousModulePairList
        }

        # send a response with the diff json structure
        return HttpResponse(json.dumps(analogousModulePairListWithDiagnosticValues), content_type="application/json")