from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

# Inlcude my API
from website.views.api import control as api_control
from website.admin import admin_site

admin.autodiscover()

#List of the website specific urls
urlpatterns = [
    url(r'^control/request_challenge/$', api_control.request_challenge),
    url(r'^control/download_magic_key/$', api_control.download_magic_key),
    url(r'^control/toggle_door/$', api_control.toggle_door),
    url(r'^control/door_status/$', api_control.door_status),

    path('admin/', admin_site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

