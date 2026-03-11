from django.contrib import admin
from .models import Flat, Complaint, Owner


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    search_fields = ['town', 'town_district', 'address', 'owner', 'owners_phonenumber', 'owner_pure_phone']

    readonly_fields = ['created_at']

    fieldsets = (
        ('Владелец', {
            'fields': ('owner', 'owners_phonenumber', 'owner_pure_phone')
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
        'owner',
        'owner_phone_display',
        'owner_pure_phone_display',
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

    def owner_phone_display(self, obj):
        return obj.owners_phonenumber or '-'

    owner_phone_display.short_description = 'Исходный номер'

    def owner_pure_phone_display(self, obj):
        if obj.owner_pure_phone:
            return str(obj.owner_pure_phone)
        return '-'

    owner_pure_phone_display.short_description = 'Нормализованный номер'

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


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phonenumber',
        'pure_phone',
        'flats_count',
        'created_at',
    ]

    search_fields = [
        'name',
        'phonenumber',
        'pure_phone',
    ]

    list_filter = [
        'created_at',
    ]

    raw_id_fields = ['flats']

    readonly_fields = ['created_at', 'updated_at', 'flats_count_display']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'phonenumber', 'pure_phone')
        }),
        ('Квартиры', {
            'fields': ('flats', 'flats_count_display'),
            'description': 'Квартиры, принадлежащие этому собственнику'
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('wide',)
        }),
    )

    list_per_page = 50

    def flats_count(self, obj):
        return obj.flats.count()

    flats_count.short_description = 'Кол-во квартир'
    flats_count.admin_order_field = 'flats'

    def flats_count_display(self, obj):
        count = obj.flats.count()
        if count == 0:
            return 'Нет квартир'
        elif count == 1:
            return '1 квартира'
        elif 2 <= count <= 4:
            return f'{count} квартиры'
        else:
            return f'{count} квартир'

    flats_count_display.short_description = 'Квартир в собственности'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('flats')