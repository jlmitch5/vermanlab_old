# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'KernelVersion.pretty_kernel_version_name'
        db.delete_column(u'schema_kernel_kernelversion', 'pretty_kernel_version_name')


    def backwards(self, orm):
        # Adding field 'KernelVersion.pretty_kernel_version_name'
        db.add_column(u'schema_kernel_kernelversion', 'pretty_kernel_version_name',
                      self.gf('django.db.models.fields.CharField')(default='kernel version', max_length=100),
                      keep_default=False)


    models = {
        u'schema_kernel.kernelversion': {
            'Meta': {'object_name': 'KernelVersion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'schema_kernel.pcialiases': {
            'Meta': {'unique_together': "(('vendor', 'subvendor', 'device', 'subdevice'),)", 'object_name': 'PCIAliases'},
            'device': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['schema_kernel.PCIModule']", 'symmetrical': 'False'}),
            'subdevice': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'subvendor': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'schema_kernel.pcimodule': {
            'Meta': {'unique_together': "(('name', 'version', 'srcversion'),)", 'object_name': 'PCIModule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kernelVersionModuleConnector': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['schema_kernel.KernelVersion']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'srcversion': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['schema_kernel']