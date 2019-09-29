from django.contrib import admin

# Register your models here.
class MyAdminSite( admin.AdminSite ):
    # Text to put at the end of each page's <title>.
    site_title = 'Garage door admin'

    # Text to put in each page's <h1>.
    site_header = 'Garage door'

    # Text to put at the top of the admin index page.
    index_title = 'Garage door admin'
admin_site = MyAdminSite()
