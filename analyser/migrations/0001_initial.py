# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Cluster'
        db.create_table('analyser_cluster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geocoded', self.gf('django.db.models.fields.TextField')()),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Device'])),
        ))
        db.send_create_signal('analyser', ['Cluster'])

        # Adding M2M table for field locations on 'Cluster'
        db.create_table('analyser_cluster_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cluster', models.ForeignKey(orm['analyser.cluster'], null=False)),
            ('location', models.ForeignKey(orm['logger.location'], null=False))
        ))
        db.create_unique('analyser_cluster_locations', ['cluster_id', 'location_id'])


    def backwards(self, orm):
        
        # Deleting model 'Cluster'
        db.delete_table('analyser_cluster')

        # Removing M2M table for field locations on 'Cluster'
        db.delete_table('analyser_cluster_locations')


    models = {
        'analyser.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['manager.Device']"}),
            'geocoded': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['logger.Location']", 'symmetrical': 'False'})
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

    complete_apps = ['analyser']
