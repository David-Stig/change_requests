from django.contrib import admin

from .models import ChangeRequest, Functionality, Ministry, System, User

admin.site.register(User)
admin.site.register(Ministry)
admin.site.register(System)
admin.site.register(Functionality)
admin.site.register(ChangeRequest)
