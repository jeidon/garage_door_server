from django.http import HttpResponse
from django.db import transaction 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt

from website.helpers.json_api import reqArgs, jsonResponse, errResponse

from website.models import MagicKey
from website.helpers import util
from time import sleep
from django.conf import settings

import json, datetime, time, re, pytz, uuid, hashlib
import RPi.GPIO as GPIO


@csrf_exempt
@reqArgs()
def request_challenge( request, *args, **kwargs ):
    challenge = util.createHash()
    answer = util.createHash( MagicKey.getMagicKey(), challenge )

    # Set the answer to the hash
    if answer == challenge or answer is None or \
       len(util.xstr(answer)) != 64 or len(util.xstr(challenge)) != 64:
        return errResponse( request, "Invalid" )

    # Store the answer into the cache engine
    cache.set("challenge_response", answer)

    return jsonResponse( request, { 'challenge': challenge })


@csrf_exempt
@reqArgs( post_req=[
              ('challenge_response', str),
          ],
)
def toggle_door( request, challenge_response, *args, **kwargs ):
    # Get the correct, answer, then delete it
    key = "challenge_response"
    correct = cache.get( key )
    cache.delete( key )

    # Ensure they had the right answer
    if correct != challenge_response or \
       len(util.xstr(correct)) != 64 or len(util.xstr(challenge_response)) != 64:
        return errResponse( request, "Invalid challenge response")

    # Drive the gpio
    pin = settings.OUTPUT_PIN
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup( pin, GPIO.OUT, initial=0)

    # This causes the button to be pushed
    GPIO.output(pin, True)
    sleep(settings.PRESS_DURATION)
    GPIO.output(pin, False)

    return jsonResponse( request, {})


@csrf_exempt
@reqArgs( post_req=[
              ('challenge_response', str),
          ],
)
def door_status( request, challenge_response, *args, **kwargs ):
    # Get the correct, answer, then delete it
    key = "challenge_response"
    correct = cache.get( key )
    cache.delete( key )

    # Ensure they had the right answer
    if correct != challenge_response or \
       len(util.xstr(correct)) != 64 or len(util.xstr(challenge_response)) != 64:
        return errResponse( request, "Invalid challenge response")

    # Drive the gpio
    pin = settings.INPUT_PIN
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup( pin, GPIO.IN)

    return jsonResponse( request, {'status': util.xbool(not GPIO.input(pin))
                                  })

@csrf_exempt
@reqArgs( post_req=[
    ('challenge', str),
],
)
def download_magic_key( request, challenge, *args, **kwargs ):
    # Get the correct, answer, then delete it
    key = "magic_key"
    result = cache.get( key )
    cache.delete( key )

    # Ensure they had the right answer
    if result != challenge:
        return errResponse( request, "Invalid challenge response")

    return jsonResponse( request, {'magic_key': MagicKey.getMagicKey()
                                   })
