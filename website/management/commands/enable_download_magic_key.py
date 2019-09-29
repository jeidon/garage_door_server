from django.core.management.base import BaseCommand

from django.core.cache import cache

import json, time, re, requests

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('challenge', type=str)

    # Run the command
    def handle(self, *args, **options):
        cache.set("magic_key", options['challenge'] )

        print( "Quickly tell the new app to type in: **%s** and download" % options['challenge'] )