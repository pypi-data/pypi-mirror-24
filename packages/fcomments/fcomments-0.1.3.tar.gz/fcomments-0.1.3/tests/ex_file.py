#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

  dependencies = [
      ('event', '0047_remove_eventreport_author'),
  ]

  operations = [
      migrations.AddField(
          model_name='eventreport',
          name='author',
          field=models.ForeignKey(to='event.EventReportAuthor', null=True, blank=True),
      ),
      migrations.AddField(
          model_name='eventreport',
          name='author1',
          field=models.ForeignKey(to='event2.EventReportAuthor', null=True, blank=True),
      ),
  ]
