# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Log'
        db.create_table('logger_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Device'])),
            ('received_date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('logger', ['Log'])

        # Adding model 'Location'
        db.create_table('logger_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logger.Log'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Device'])),
            ('speed', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=1)),
            ('heading', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('altitude', self.gf('django.db.models.fields.FloatField')()),
            ('accuracy', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('sent_date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('sos', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('logger', ['Location'])

        # Adding model 'BatteryCharge'
        db.create_table('logger_batterycharge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logger.Log'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Device'])),
            ('battery_percentage', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('sent_date_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('logger', ['BatteryCharge'])

        # Adding model 'DeviceEvent'
        db.create_table('logger_deviceevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logger.Log'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Device'])),
            ('sent_date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('event', self.gf('django.db.models.fields.CharField')(max_length='50')),
        ))
        db.send_create_signal('logger', ['DeviceEvent'])


    def backwards(self, orm):
        
        # Deleting model 'Log'
        db.delete_table('logger_log')

        # Deleting model 'Location'
        db.delete_table('logger_location')

        # Deleting model 'BatteryCharge'
        db.delete_table('logger_batterycharge')

        # Deleting model 'DeviceEvent'
        db.delete_table('logger_deviceevent')


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
            'imei': ('django.db.models.fields.CharField', [], {'max_length': '19'}),
            'local_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'received_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['logger']
