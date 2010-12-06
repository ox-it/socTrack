# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Cluster.speed'
        db.add_column('analyser_cluster', 'speed', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=1), keep_default=False)

        # Adding field 'Cluster.altitude'
        db.add_column('analyser_cluster', 'altitude', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'Cluster.location'
        db.add_column('analyser_cluster', 'location', self.gf('django.contrib.gis.db.models.fields.PointField')(default=(0, 0)), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Cluster.speed'
        db.delete_column('analyser_cluster', 'speed')

        # Deleting field 'Cluster.altitude'
        db.delete_column('analyser_cluster', 'altitude')

        # Deleting field 'Cluster.location'
        db.delete_column('analyser_cluster', 'location')


    models = {
        'analyser.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'altitude': ('django.db.models.fields.FloatField', [], {}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Device']"}),
            'geocoded': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['logger.Location']", 'symmetrical': 'False'}),
            'speed': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '1'})
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
            'cause': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.SMS']", 'null': 'True'}),
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

    complete_apps = ['analyser']
