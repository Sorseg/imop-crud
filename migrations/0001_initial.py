# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Student'
        db.create_table('students_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('first_name_lat', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name_lat', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('citizenship', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('passport_num', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('passport_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('contract_status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('program_status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('expected_program', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('e_mail', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('note', self.gf('django.db.models.fields.TextField')()),
            ('register_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('arrival_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=511)),
        ))
        db.send_create_signal('students', ['Student'])

        # Adding model 'StudentRecordLock'
        db.create_table('students_studentrecordlock', (
            ('record', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['students.Student'], unique=True, primary_key=True)),
            ('locked_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('locked_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('students', ['StudentRecordLock'])


    def backwards(self, orm):
        # Deleting model 'Student'
        db.delete_table('students_student')

        # Deleting model 'StudentRecordLock'
        db.delete_table('students_studentrecordlock')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'students.student': {
            'Meta': {'object_name': 'Student'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '511'}),
            'arrival_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'citizenship': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contract_status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'e_mail': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expected_program': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name_lat': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_name_lat': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'passport_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'passport_num': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'program_status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'register_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'students.studentrecordlock': {
            'Meta': {'object_name': 'StudentRecordLock'},
            'locked_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'locked_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'record': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['students.Student']", 'unique': 'True', 'primary_key': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['students']