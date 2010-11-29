# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Location.analysed'
        db.add_column('logger_location', 'analysed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Location.analysed'
        db.delete_column('logger_location', 'analysed')


    models = {
        'logger.batterycharge': {
            'Meta': {'object_name': 'BatteryCharge'},
            'battery_percentage': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logger.Log']"}),
            'sent_date_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'logger.deviceevent': {
            'Meta': {'object_name': 'DeviceEvent'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Device']"}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logger.Log']"}),
            'sent_date_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'logger.location': {
            'Meta': {'object_name': 'Location'},
            'accuracy': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'analysed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Device']"}),
            'heading': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['logger.Log']"}),
            'sent_date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'sos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'speed': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '1'})
        },
        'logger.log': {
            'Meta': {'object_name': 'Log'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'received_date_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'manager.device': {
            'Meta': {'object_name': 'Device'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '19'}),
            'local_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'received_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['logger']
