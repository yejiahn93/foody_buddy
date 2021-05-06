from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from django.contrib import admin
from .models import Restaurant

admin.site.register(Restaurant)

class ResaturantAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {
          'address': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
    }