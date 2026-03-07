from django.contrib import admin
from .models import Device, ScanResults, Alert

admin.site.register(Device)
admin.site.register(ScanResults)
admin.site.register(Alert)