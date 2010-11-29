# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'Device', fields ['imei']
        db.create_unique('manager_device', ['imei'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Device', fields ['imei']
        db.delete_unique('manager_device', ['imei'])


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
            'imei': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '19'}),
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
