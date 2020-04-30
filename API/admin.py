from django.contrib import admin
from .models import Announcement, Doctor, MarkedPlaces, PassportInfo, UpdateSummary

# Register your models here.

admin.site.register(Announcement)
admin.site.register(Doctor)
admin.site.register(MarkedPlaces)
admin.site.register(PassportInfo)
admin.site.register(UpdateSummary)
