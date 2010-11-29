# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Network'
        db.create_table('manager_network', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('manager', ['Network'])

        # Adding model 'Device'
        db.create_table('manager_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imei', self.gf('django.db.models.fields.CharField')(max_length=19)),
            ('local_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('received_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('manager', ['Device'])

        # Adding model 'Sim'
        db.create_table('manager_sim', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sim_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Network'])),
            ('data_plan_expiry', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contract', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('manager', ['Sim'])

        # Adding model 'Deployment'
        db.create_table('manager_deployment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Device'])),
            ('sim', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Sim'])),
            ('post_out_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('received_back_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('survey_start', self.gf('django.db.models.fields.DateField')()),
            ('survey_end', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('manager', ['Deployment'])


    def backwards(self, orm):
        
        # Deleting model 'Network'
        db.delete_table('manager_network')

        # Deleting model 'Device'
        db.delete_table('manager_device')

        # Deleting model 'Sim'
        db.delete_table('manager_sim')

        # Deleting model 'Deployment'
        db.delete_table('manager_deployment')


    models = {
        'manager.deployment': {
            'Meta': {'object_name': 'Deployment'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_out_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'received_back_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sim': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Sim']"}),
            'survey_end': ('django.db.models.fields.DateField', [], {}),
            'survey_start': ('django.db.models.fields.DateField', [], {})
        },
        'manager.device': {
            'Meta': {'object_name': 'Device'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'max_length': '19'}),
            'local_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'received_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'manager.network': {
            'Meta': {'object_name': 'Network'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'manager.sim': {
            'Meta': {'object_name': 'Sim'},
            'contract': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'data_plan_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Network']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sim_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['manager']
