# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Device.password'
        db.add_column('manager_device', 'password', self.gf('django.db.models.fields.CharField')(default='gl100', max_length=8), keep_default=False)

        # Adding field 'SMS.human_message'
        db.add_column('manager_sms', 'human_message', self.gf('django.db.models.fields.TextField')(default='', max_length=160, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Device.password'
        db.delete_column('manager_device', 'password')

        # Deleting field 'SMS.human_message'
        db.delete_column('manager_sms', 'human_message')


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
            'password': ('django.db.models.fields.CharField', [], {'default': "'gl100'", 'max_length': '8'}),
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
