from django.contrib import admin
from .models import Vendor, OpeningHour
# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user','vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user','vendor_name')
    list_editable = ('is_approved',)


class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('vendor','from_hour', 'to_hour', 'is_closed')
    
    
admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHoursAdmin)