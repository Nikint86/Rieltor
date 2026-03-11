from django.contrib import admin
from .models import Flat, Complaint


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    search_fields = ['town', 'town_district', 'address', 'owner']

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
        ('Лайки', {
            'fields': ('liked_by',),
            'description': 'Пользователи, которым понравилась эта квартира'
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
        'likes_count',
    ]

    list_editable = ['new_building', 'price']

    list_filter = [
        'new_building',
        'active',
        'town',
        'rooms_number',
        'has_balcony',
        'construction_year',
    ]

    raw_id_fields = ['liked_by']

    list_per_page = 20

    def likes_count(self, obj):
        return obj.liked_by.count()

    likes_count.short_description = 'Кол-во лайков'
    likes_count.admin_order_field = 'liked_by'


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['user', 'flat', 'short_text', 'created_at']
    list_filter = ['created_at', 'user']

    raw_id_fields = ['user', 'flat']

    readonly_fields = ['created_at']

    search_fields = ['text', 'user__username', 'flat__address']

    list_per_page = 50

    def short_text(self, obj):
        if len(obj.text) > 50:
            return obj.text[:50] + '...'
        return obj.text

    short_text.short_description = 'Текст жалобы'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'flat')