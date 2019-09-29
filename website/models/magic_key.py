from django.db import models
from django.contrib import admin
from django.conf import settings

from website.helpers import util

# Defines an object whos duty is to hold pay rate information
class MagicKey(models.Model):
    # Define my models
    id              = models.AutoField(primary_key=True)

    magic_key       = models.CharField(max_length=128, help_text="The magic key")

    updated_on      = models.DateTimeField(auto_now=True)
    created_on      = models.DateTimeField(auto_now_add=True)


    class Meta:
        app_label = 'website'


    #Returns a friendly name for the admin interface
    def __str__(self):
        return "%s" % (self.magic_key)


    @staticmethod
    def getMagicKey():
        keys = list(MagicKey.objects.all().order_by("created_on"))
        while len(keys) > 1:
            del keys[0]

        return keys[0].magic_key if len(keys) > 0 else MagicKey.createMagicKey().magic_key


    @staticmethod
    def createMagicKey():
        obj = MagicKey(magic_key=util.createHash())
        obj.save()

        return obj


    #Convert my data to json
    def toJson(self):
        return {'magic_key':        str(self.magic_key),
               }

    @staticmethod
    def customAdmin( idx=0 ):
        class MagicKey(admin.ModelAdmin):
            pass

        return ( MagicKey, None )[idx]
