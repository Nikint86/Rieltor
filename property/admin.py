from django.contrib import admin
from .models import Flat, Complaint, Owner


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    search_fields = ['town', 'town_district', 'address', 'owners__name', 'owners__phonenumber']

    readonly_fields = ['created_at']

    fieldsets = (
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
        ('Собственники', {
            'fields': ('owners',),
            'description': 'Собственники этой квартиры'
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
        'get_owners_names',
        'get_owners_phones',
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

    raw_id_fields = ['liked_by', 'owners']

    list_per_page = 20

    def get_owners_names(self, obj):
        return ", ".join([owner.name for owner in obj.owners.all()[:3]])

    get_owners_names.short_description = 'Собственники'

    def get_owners_phones(self, obj):
        phones = []
        for owner in obj.owners.all()[:3]:
            if owner.pure_phone:
                phones.append(str(owner.pure_phone))
            elif owner.phonenumber:
                phones.append(owner.phonenumber)
        return ", ".join(phones)

    get_owners_phones.short_description = 'Телефоны'

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
        'flats_preview',
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

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'phonenumber', 'pure_phone'),
            'description': 'Основные данные о собственнике'
        }),
        ('Квартиры в собственности', {
            'fields': ('flats',),
            'description': 'Квартиры, принадлежащие этому собственнику'
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('wide',),
        }),
    )

    list_per_page = 50
    date_hierarchy = 'created_at'

    def flats_count(self, obj):
        return obj.flats.count()

    flats_count.short_description = 'Кол-во квартир'
    flats_count.admin_order_field = 'flats'

    def flats_preview(self, obj):
        flats = obj.flats.all()[:3]
        if flats:
            return ', '.join([flat.address[:30] + '...' if len(flat.address) > 30 else flat.address for flat in flats])
        return '-'

    flats_preview.short_description = 'Квартиры'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('flats')