# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KernelVersion'
        db.create_table(u'schema_kernel_kernelversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('pretty_kernel_version_name', self.gf('django.db.models.fields.CharField')(default='kernel version', max_length=100)),
        ))
        db.send_create_signal(u'schema_kernel', ['KernelVersion'])

        # Adding model 'PCIModule'
        db.create_table(u'schema_kernel_pcimodule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('srcversion', self.gf('django.db.models.fields.CharField')(max_length=24, null=True, blank=True)),
        ))
        db.send_create_signal(u'schema_kernel', ['PCIModule'])

        # Adding unique constraint on 'PCIModule', fields ['name', 'version', 'srcversion']
        db.create_unique(u'schema_kernel_pcimodule', ['name', 'version', 'srcversion'])

        # Adding M2M table for field kernelVersionModuleConnector on 'PCIModule'
        m2m_table_name = db.shorten_name(u'schema_kernel_pcimodule_kernelVersionModuleConnector')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pcimodule', models.ForeignKey(orm[u'schema_kernel.pcimodule'], null=False)),
            ('kernelversion', models.ForeignKey(orm[u'schema_kernel.kernelversion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pcimodule_id', 'kernelversion_id'])

        # Adding model 'PCIAliases'
        db.create_table(u'schema_kernel_pcialiases', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('subvendor', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('device', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('subdevice', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'schema_kernel', ['PCIAliases'])

        # Adding unique constraint on 'PCIAliases', fields ['vendor', 'subvendor', 'device', 'subdevice']
        db.create_unique(u'schema_kernel_pcialiases', ['vendor', 'subvendor', 'device', 'subdevice'])

        # Adding M2M table for field module on 'PCIAliases'
        m2m_table_name = db.shorten_name(u'schema_kernel_pcialiases_module')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pcialiases', models.ForeignKey(orm[u'schema_kernel.pcialiases'], null=False)),
            ('pcimodule', models.ForeignKey(orm[u'schema_kernel.pcimodule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pcialiases_id', 'pcimodule_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PCIAliases', fields ['vendor', 'subvendor', 'device', 'subdevice']
        db.delete_unique(u'schema_kernel_pcialiases', ['vendor', 'subvendor', 'device', 'subdevice'])

        # Removing unique constraint on 'PCIModule', fields ['name', 'version', 'srcversion']
        db.delete_unique(u'schema_kernel_pcimodule', ['name', 'version', 'srcversion'])

        # Deleting model 'KernelVersion'
        db.delete_table(u'schema_kernel_kernelversion')

        # Deleting model 'PCIModule'
        db.delete_table(u'schema_kernel_pcimodule')

        # Removing M2M table for field kernelVersionModuleConnector on 'PCIModule'
        db.delete_table(db.shorten_name(u'schema_kernel_pcimodule_kernelVersionModuleConnector'))

        # Deleting model 'PCIAliases'
        db.delete_table(u'schema_kernel_pcialiases')

        # Removing M2M table for field module on 'PCIAliases'
        db.delete_table(db.shorten_name(u'schema_kernel_pcialiases_module'))


    models = {
        u'schema_kernel.kernelversion': {
            'Meta': {'object_name': 'KernelVersion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'pretty_kernel_version_name': ('django.db.models.fields.CharField', [], {'default': "'kernel version'", 'max_length': '100'})
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