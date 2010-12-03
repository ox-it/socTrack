# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Deployment.name'
        db.add_column('manager_deployment', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Adding field 'Deployment.contact'
        db.add_column('manager_deployment', 'contact', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Deployment.name'
        db.delete_column('manager_deployment', 'name')

        # Deleting field 'Deployment.contact'
        db.delete_column('manager_deployment', 'contact')


    models = {
        'manager.deployment': {
            'Meta': {'object_name': 'Deployment'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'post_out_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'received_back_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sim': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Sim']"}),
            'survey_end': ('django.db.models.fields.DateField', [], {}),
            'survey_start': ('django.db.models.fields.DateField', [], {})
        },
        'manager.device': {
            'Meta': {'object_name': 'Device'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '19'}),
            'local_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "'gl100'", 'max_length': '8', 'blank': 'True'}),
            'received_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'manager.network': {
            'Meta': {'object_name': 'Network'},
            'apn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'apn_password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'apn_username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'manager.sim': {
            'Meta': {'object_name': 'Sim'},
            'contract': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'data_plan_expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Network']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sim_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'manager.sms': {
            'Meta': {'object_name': 'SMS'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Device']"}),
            'human_message': ('django.db.models.fields.TextField', [], {'max_length': '160', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True'}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {}),
            'sim': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Sim']"})
        }
    }

    complete_apps = ['manager']
