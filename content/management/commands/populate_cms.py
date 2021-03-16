import re
import os
import json
import requests
import subprocess
from math import ceil
from pathlib import Path

from django.core import management
import azure.cosmos.cosmos_client as cosmos_client
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


from wagtail.core.models import Page
from core.command import SimpleCommand
from core.mongo import Mongo

from django.conf import settings


class Command(SimpleCommand):
    help = 'Populates Postgres using the data in the CMS fixture folder'

    db_host                 = ['db', '0.0.0.0', 'localhost']
    db_name                 = 'django'
    db_user                 = 'docker'
    db_password             = 'docker'
    json_file               = 'CMS/fixtures/postgres.json'
    message_count           = None
    total_success_messages  = 6


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(os.environ.get('DBHOST') not in self.db_host)
        print(os.environ.get('DBNAME') != self.db_name)
        print(os.environ.get('DBUSER') != self.db_user)
        print(os.environ.get('DBPASSWORD') != self.db_password)

        if os.environ.get('DBHOST') not in self.db_host or \
           os.environ.get('DBNAME') != self.db_name or \
           os.environ.get('DBUSER') != self.db_user or \
           os.environ.get('DBPASSWORD') != self.db_password:
            raise CommandError('DBHOST, DBNAME, DBUSER & DBPASSWORD should ' + \
                'be pointing to the local PostgresSQL')

        self.message_count = 1
        self.json_file = str(Path(self.json_file))


    def handle(self, *args, **options):

        management.call_command(
            'flush_db',
            '--allow-cascade',
            '--no-input'
        )
        self.success('Flushed database')

        management.call_command('migrate')
        self.success('Migrated database')

        Page.objects.all().delete()
        self.success('Deleted all Page rows')

        ContentType.objects.all().delete()
        self.success('Deleted all ContentType rows')

        management.call_command('loaddata', self.json_file)
        self.success('Loaded file (' + self.json_file + ')')

        self.success('Population complete')


    def success(self, message):
        super().success('[' + str(self.message_count) + ' of ' + \
            str(self.total_success_messages) + '] ' + message)
        self.message_count += 1
