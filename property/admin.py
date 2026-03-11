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
            'fields': ('price', 'rooms_number', 'living_area', 'has_balcony', 'construction_year')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'active'),
            'classes': ('wide',)
        }),
    )

    list_display = ('address', 'town', 'price', 'rooms_number', 'active', 'created_at')

    list_filter = ('active', 'town', 'rooms_number', 'has_balcony')