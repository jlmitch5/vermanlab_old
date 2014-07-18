from django.test import TestCase
from django.test.client import Client

from django.db import IntegrityError

from schema_kernel.models import KernelVersion, PCIModule, PCIAliases
from pci_ids.models import pciam
# from schema_kernel.views import GetKernelVersions

# Tests for the schema_kernel models
class SchemaKernelModelsTestCase(TestCase):
    def setUp(self):
        testKernelVersion = KernelVersion.objects.create(name="TestKernelVersion")
        testModule = PCIModule.objects.create(name="TestModule", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        testModule.kernelVersionModuleConnector.add(testKernelVersion)
        testAlias = PCIAliases.objects.create(vendor="1234", device="5678", subvendor="912", subdevice="null")
        testAlias.module.add(testModule)

    def testDuplicateModules(self):
        errorOccured = False
        try:
            duplicateModule = PCIModule.objects.create(name="TestModule", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        except IntegrityError:
            errorOccured = True

        self.assertTrue(errorOccured)

    def testDuplicateModuleNameForKernelVersion(self):
        errorOccured = False
        try:
            originalKernelVersion = KernelVersion.objects.get(name="TestKernelVersion")
            duplicateModule = PCIModule.objects.create(name="TestModule", version="2.0", srcversion="128E7DBE00BCDAD0108DE5B")
            duplicateModule.save
            duplicateModule.kernelVersionModuleConnector.add(originalKernelVersion)
        except IntegrityError:
            errorOccured = True

#        self.assertTrue(errorOccured)
         self.assertTrue(false)

    def testUnicodeModule(self):
        testModule = PCIModule.objects.create(name="TestModule", version="1.0", srcversion="NULL")
        self.assertEquals(testModule.__unicode__(), u"TestModule 1.0")
        testModule2 = PCIModule.objects.create(name="TestModule", version="2.0", srcversion="128E7DBE00BCDAD0108DE5B")
        self.assertEquals(testModule2.__unicode__(), u"TestModule 2.0 128E7DBE00BCDAD0108DE5B")

    def testDuplicateAliasesWithNulls(self):
        errorOccured = False
        try:
            testAlias1 = PCIAliases.objects.create(vendor="1234", device="5678", subvendor="null", subdevice="null")
            testAlias2 = PCIAliases.objects.create(vendor="1234", device="5678", subvendor="null", subdevice="null")
        except IntegrityError:
            errorOccured = True
        self.assertTrue(errorOccured)

    def testUnicodeAlias(self):
        testAlias = PCIAliases.objects.get(vendor="1234", device="5678", subvendor="912", subdevice="null")
        self.assertEquals(testAlias.__unicode__(), u"1234:5678:0912")
        testAlias2 = PCIAliases.objects.create(vendor="1234", device="5678", subvendor="9128", subdevice="0000")
        self.assertEquals(testAlias2.__unicode__(), u"1234:5678:9128:0000")

# Test for GetKernelVersions api call
class GetKernelVersionsTestCase(TestCase):
    def setUp(self):
        KernelVersion.objects.create(name="TestKernelVersion")
        KernelVersion.objects.create(name="TestKernelVersion2")
        KernelVersion.objects.create(name="TestKernelVersion3")
        self.c = Client()

    def testGetKernelVersions(self):
        response = self.c.get('/api/get_kernel_versions/', format='json')
        expectedResponse = '[{"name": "TestKernelVersion"}, {"name": "TestKernelVersion2"}, {"name": "TestKernelVersion3"}]'
        self.assertEquals(response.content, expectedResponse)

# Test for Diff api call
class DiffTestCase(TestCase):
    def setUp(self):
        self.testKernelVersion1 = KernelVersion.objects.create(name="TestKernelVersion1")
        self.testKernelVersion2 = KernelVersion.objects.create(name="TestKernelVersion2")

        self.testModuleOnlyKernel1 = PCIModule.objects.create(name="TestModuleKernel1", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        self.testModuleOnlyKernel1.kernelVersionModuleConnector.add(self.testKernelVersion1)

        self.testModuleOnlyKernel2 = PCIModule.objects.create(name="TestModuleKernel2", version="1.0", srcversion="23857DBE00BCDAD0108DE5A")
        self.testModuleOnlyKernel2.kernelVersionModuleConnector.add(self.testKernelVersion2)

        self.c = Client()

    def testDiffModules(self):
        # populate the schema with different module combinations
        testModuleBothKernels = PCIModule.objects.create(name="TestModuleKernelBoth", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        testModuleBothKernels.kernelVersionModuleConnector.add(self.testKernelVersion1)
        testModuleBothKernels.kernelVersionModuleConnector.add(self.testKernelVersion2)
        testDiffModuleBothKernels = PCIModule.objects.create(name="TestDiffModuleKernelBoth", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        testDiffModuleBothKernels.kernelVersionModuleConnector.add(self.testKernelVersion1)
        testDiffModuleBothKernels2 = PCIModule.objects.create(name="TestDiffModuleKernelBoth", version="NULL", srcversion="NULL")
        testDiffModuleBothKernels2.kernelVersionModuleConnector.add(self.testKernelVersion2)
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel2Alias = PCIAliases.objects.create(vendor="9710", device="9815", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel2Alias.module.add(self.testModuleOnlyKernel2)
        response = self.c.get('/api/diff/'+self.testKernelVersion1.name+'/'+self.testKernelVersion2.name+'/', format='json')
        expectedResponse = '{"mods": [{"k1m": {"a": [], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestDiffModuleKernelBoth", "kv": "TestKernelVersion1", "v": "1.0"}, "k2m": {"a": [], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestDiffModuleKernelBoth", "kv": "TestKernelVersion2", "v": "1.0"}}, {"k1m": {"a": [], "srcv": "128E7DBE00BCDAD0108DE5A", "m": "TestModuleKernel1", "kv": "TestKernelVersion1", "v": "1.0"}, "k2m": null}, {"k1m": null, "k2m": {"a": [], "srcv": "23857DBE00BCDAD0108DE5A", "m": "TestModuleKernel2", "kv": "TestKernelVersion2", "v": "1.0"}}], "kv2m": 0, "kv1v": 0, "kv1m": 0, "kv2v": 0, "dv": 1}'
        print response.content

    def testDiffAliases(self):
        pciam.objects.create(val="aa55", v="Ncomputing X300 PCI-Engine")
        pciam.objects.create(val="103c:323b:103c:3354", v="Hewlett-Packard Company", d="Smart Array Gen8 Controllers", s="P420i")
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel1Alias = PCIAliases.objects.create(vendor="9710", device="9815", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel1Alias.module.add(self.testModuleOnlyKernel1)
        # this one has that non-descriptive "1234" vendor
        testModuleOnlyKernel1Alias1234 = PCIAliases.objects.create(vendor="1234", device="9815", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel1Alias1234.module.add(self.testModuleOnlyKernel1)
        # this module only has vendor and device (and the device isn't valid)
        testModuleOnlyKernel1AliasVendorDevice = PCIAliases.objects.create(vendor="aa55", device="4x36")
        testModuleOnlyKernel1AliasVendorDevice.module.add(self.testModuleOnlyKernel1)
        # this module only has vendor and device (and neither is valid)
        testModuleOnlyKernel1AliasVendorDeviceNotExist = PCIAliases.objects.create(vendor="haha", device="4x36")
        testModuleOnlyKernel1AliasVendorDeviceNotExist.module.add(self.testModuleOnlyKernel1)
        # this module has the full alias to human-readable device map
        testModuleOnlyKernel1HasFullDeviceName = PCIAliases.objects.create(vendor="103c", device="323b", subvendor="103c", subdevice="3354")
        testModuleOnlyKernel1HasFullDeviceName.module.add(self.testModuleOnlyKernel1)
        response = self.c.get('/api/diff/'+self.testKernelVersion1.name+'/'+self.testKernelVersion2.name+'/', format='json')
        print response.content

    def testDiffCounters(self):
        kernelModuleVersion1Counter = 1
        kernelModuleVersion2Counter = 2
        testDiffModuleBothKernels = PCIModule.objects.create(name="TestDiffModuleKernelBoth", version="1.0", srcversion="128E7DBE00BCDAD0108DE5A")
        testDiffModuleBothKernels.kernelVersionModuleConnector.add(self.testKernelVersion1)
        testDiffModuleBothKernels2 = PCIModule.objects.create(name="TestDiffModuleKernelBoth", version="NULL", srcversion="NULL")
        testDiffModuleBothKernels2.kernelVersionModuleConnector.add(self.testKernelVersion2)
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel1AliasForDiff = PCIAliases.objects.create(vendor="9710", device="9815", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel1AliasForDiff.module.add(testDiffModuleBothKernels)
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel2AliasForDiff = PCIAliases.objects.create(vendor="9710", device="9835", subvendor = "1000", subdevice="0020")
        testModuleOnlyKernel2AliasForDiff.module.add(testDiffModuleBothKernels2)
        # just a regular alias (with human-readable device mapping)
        testModuleOnlyKernel2AliasForDiff2 = PCIAliases.objects.create(vendor="9710", device="9815")
        testModuleOnlyKernel2AliasForDiff2.module.add(testDiffModuleBothKernels2)
        response = self.c.get('/api/diff/'+self.testKernelVersion1.name+'/'+self.testKernelVersion2.name+'/', format='json')
        print response.content










