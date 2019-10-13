from django.core.management.base import BaseCommand

from django.conf import settings
from django.core.cache import cache
from twilio.rest import Client
from website.helpers import util
from time import sleep
import RPi.GPIO as GPIO

# Create a systemd script to run this every minute
'''
'''

class Command(BaseCommand):
    help = 'Check for state change in the garage door, alert the user if it changed'

    #def add_arguments(self, parser):
    #    parser.add_argument('challenge', type=str)

    # Run the command
    def handle(self, *args, **options):
        # Get the cache, and the current door status
        key = 'garage_door_status'
        last_status = cache.get( key )

        # Drive the gpio
        pin = settings.INPUT_PIN
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( pin, GPIO.IN, pull_up_down=GPIO.PUD_UP )
        sleep( 0.2 )
        status = not util.xbool( GPIO.input( settings.INPUT_PIN ) )

        # Update the cache
        cache.set( key, status )

        # Don't do anything
        if last_status == status:
            print("No change!")
            return

        # Send out messages
        msg = "Garage door %s" % ("closed" if status else "opened")
        client = Client( settings.TWILIO_SID, settings.TWILIO_TOKEN )

        for to in settings.TWILIO_TO:
            client.messages.create(
                body=msg,
                from_=settings.TWILIO_FROM,
                to=to,
            )

