from django.contrib import admin
from test1api.models import users

class usersAdmin(admin.ModelAdmin):
    list_display=('uid','question')
admin.site.register(users, usersAdmin)
