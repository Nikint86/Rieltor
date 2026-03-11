from django.contrib import admin
from .models import Flat


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    search_fields = ['town', 'town_district', 'address']

    readonly_fields = ['created_at']

    fieldsets = (
        ('Владелец', {
            'fields': ('owner', 'owners_phonenumber')
        }),
        ('Адрес', {
            'fields': ('town', 'town_district', 'address', 'floor')
        }),
        ('Характеристики', {
            'fields': ('price', 'rooms_number', 'living_area', 'has_balcony',
                       'construction_year', 'new_building')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'active'),
            'classes': ('wide',)
        }),
    )

    list_display = [
        'address',
        'price',
        'new_building',
        'construction_year',
        'town',
    ]

    list_editable = ['new_building', 'price']

    list_filter = ['new_building', 'town', 'active']

    list_per_page = 20