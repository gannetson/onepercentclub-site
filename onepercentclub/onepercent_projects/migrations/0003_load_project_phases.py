# -*- coding: utf-8 -*-
from south.v2 import DataMigration
from django.core.management import call_command


class Migration(DataMigration):

    def forwards(self, orm):
        call_command("loaddata", 'booking_project_phases')

    def backwards(self, orm):
        #This migration only adds data
        pass;
