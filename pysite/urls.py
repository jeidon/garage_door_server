from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

# Inlcude my API
from website.views.api import avatar as api_avatar
from website.views.api import capture as api_capture
from website.views.api import course as api_course
from website.views.api import device as api_device
from website.views.api import feed as api_feed
from website.views.api import friends as api_friends
from website.views.api import klass as api_klass
from website.views.api import leader_board as api_leader_board
from website.views.api import points as api_points
from website.views.api import radius as api_radius
from website.views.api import registration as api_registration
from website.views.api import user as api_user
from website.admin import admin_site

admin.autodiscover()

#List of the website specific urls
urlpatterns = [
    url(r'^avatar/list/$', api_avatar.list),
    url(r'^avatar/user_avatar/$', api_avatar.user_avatar),

    url(r'^capture/create/$', api_capture.create),
    url(r'^capture/complete/$', api_capture.complete),
    url(r'^capture/assign_device/$', api_capture.assign_device),
    url(r'^capture/remove_device/$', api_capture.remove_device),
    url(r'^capture/assign_radius/$', api_capture.assign_radius),
    url(r'^capture/remove_radius/$', api_capture.remove_radius),
    url(r'^capture/list/$', api_capture.list),
    url(r'^capture/download_active_capture', api_capture.download_active_capture),
    url(r'^capture/download/$', api_capture.download),

    url(r'^course/create/$', api_course.create),
    url(r'^course/create_section/$', api_course.create_section),
    url(r'^course/capture_to_section/$', api_course.capture_to_section),
    url(r'^course/create_vcps/$', api_course.create_vcps),
    url(r'^course/remove_vcp/$', api_course.remove_vcp),
    url(r'^course/create_points/$', api_course.create_points),
    url(r'^course/remove_points/$', api_course.remove_points),
    url(r'^course/retrieve/$', api_course.retrieve),

    url(r'^device/create/$', api_device.create),
    url(r'^device/modify/$', api_device.modify),
    url(r'^device/is_push_token_valid/$', api_device.is_push_token_valid),

    url(r'^feed/mixed/$', api_feed.mixed),

    url(r'^friends/list/$', api_friends.list),
    url(r'^friends/assign_friendship/$', api_friends.assign_friendship),
    url(r'^friends/assign_notify/$', api_friends.assign_notify),

    url(r'^klass/create/$', api_klass.create),
    url(r'^klass/modify/$', api_klass.modify),
    url(r'^klass/remove/$', api_klass.remove),

    url(r'^leader_board/view/$', api_leader_board.view),

    url(r'^points/store/$', api_points.store),
    url(r'^points/backfill/$', api_points.backfill),
    url(r'^points/retrieve_everyone/$', api_points.retrieve_everyone),
    url(r'^points/retrieve_radius/$', api_points.retrieve_radius),
    url(r'^points/retrieve_user/$', api_points.retrieve_user),

    url(r'^radius/create/$', api_radius.create),
    url(r'^radius/list/$', api_radius.connected_radii),
    url(r'^radius/near_me/$', api_radius.near_me),
    url(r'^radius/desc/$', api_radius.desc),
    url(r'^radius/bulk_desc/$', api_radius.bulk_desc),

    url(r'^registration/create/$', api_registration.create),
    url(r'^registration/destroy/$', api_registration.destroy),

    url(r'^user/create/$', api_user.create),
    url(r'^user/auth/$', api_user.auth),
    url(r'^user/recovery_auth/$', api_user.recovery_auth),
    url(r'^user/is_unique/$', api_user.is_unique),
    url(r'^user/is_access_code_valid/$', api_user.is_access_code_valid),
    url(r'^user/modify/$', api_user.modify),
    url(r'^user/add_activity/$', api_user.add_activity),
    url(r'^user/remove_activity/$', api_user.remove_activity),
    url(r'^user/generate_access_code/$', api_user.generate_access_code),
    url(r'^user/generate_recovery_access_code/$', api_user.generate_recovery_access_code),
    url(r'^user/summary/$', api_user.summary),

    path('admin/', admin_site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

