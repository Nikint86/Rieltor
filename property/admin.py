from django.contrib import admin
from .models import Flat, Complaint, Owner


class FlatOwnerInline(admin.TabularInline):
    model = Flat.owners.through
    verbose_name = 'Собственник'
    verbose_name_plural = 'Собственники'

    raw_id_fields = ['owner']

    fields = ['owner', 'owner_info']
    readonly_fields = ['owner_info']

    extra = 1

    can_delete = True

    def owner_info(self, obj):
        if obj.owner_id:
            owner = obj.owner
            phone = owner.pure_phone or owner.phonenumber or 'Нет телефона'
            flats_count = owner.flats.count()
            return f"📞 {phone} | Квартир: {flats_count}"
        return "Выберите собственника"

    owner_info.short_description = 'Информация'


class FlatOwnerStackedInline(admin.StackedInline):
    model = Flat.owners.through
    verbose_name = 'Собственник'
    verbose_name_plural = 'Собственники'

    raw_id_fields = ['owner']

    fields = [
        'owner',
        'owner_details',
        'owner_contacts',
    ]

    readonly_fields = ['owner_details', 'owner_contacts']

    extra = 1
    can_delete = True

    def owner_details(self, obj):
        if obj.owner_id:
            owner = obj.owner
            flats_count = owner.flats.count()
            flats_list = ', '.join([f"кв.{flat.id}" for flat in owner.flats.all()[:3]])
            if owner.flats.count() > 3:
                flats_list += f" и еще {owner.flats.count() - 3}"
            return f"Квартир в собственности: {flats_count}\nАдреса: {flats_list}"
        return "Нет информации"

    owner_details.short_description = 'Детали'

    def owner_contacts(self, obj):
        if obj.owner_id:
            owner = obj.owner
            phones = []
            if owner.pure_phone:
                phones.append(f"📱 {owner.pure_phone}")
            if owner.phonenumber:
                phones.append(f"📞 {owner.phonenumber}")
            return '\n'.join(phones) if phones else 'Нет контактов'
        return 'Нет контактов'

    owner_contacts.short_description = 'Контакты'


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    inlines = [FlatOwnerInline]

    search_fields = ['town', 'town_district', 'address', 'owners__name', 'owners__phonenumber']

    readonly_fields = ['created_at', 'get_owners_list']

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
            'fields': ('get_owners_list', 'owners'),
            'description': 'Собственники этой квартиры (можно выбрать несколько)'
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
        'get_owners_count',
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

    def get_owners_list(self, obj):
        owners = obj.owners.all()
        if not owners:
            return "Нет собственников"

        result = []
        for owner in owners:
            phone = owner.pure_phone or owner.phonenumber or 'нет телефона'
            result.append(f"• {owner.name} — {phone}")

        return "<br>".join(result)

    get_owners_list.short_description = 'Список собственников'
    get_owners_list.allow_tags = True

    def get_owners_names(self, obj):
        return ", ".join([owner.name for owner in obj.owners.all()[:3]])

    get_owners_names.short_description = 'Собственники'

    def get_owners_count(self, obj):
        count = obj.owners.count()
        return f"{count} собств." if count else "-"

    get_owners_count.short_description = 'Кол-во'

    def likes_count(self, obj):
        return obj.liked_by.count()

    likes_count.short_description = 'Лайки'
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

    readonly_fields = ['created_at', 'updated_at', 'flats_list']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'phonenumber', 'pure_phone'),
            'description': 'Основные данные о собственнике'
        }),
        ('Квартиры в собственности', {
            'fields': ('flats', 'flats_list'),
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
            addresses = []
            for flat in flats:
                short_addr = flat.address[:30] + '...' if len(flat.address) > 30 else flat.address
                addresses.append(f"{short_addr} ({flat.price}р.)")
            return ', '.join(addresses)
        return '-'

    flats_preview.short_description = 'Квартиры'

    def flats_list(self, obj):
        flats = obj.flats.all()
        if not flats:
            return "Нет квартир"

        result = ['<table style="width:100%">']
        result.append('<tr><th>ID</th><th>Адрес</th><th>Цена</th><th>Город</th></tr>')

        for flat in flats:
            result.append(f'<tr>')
            result.append(f'<td>{flat.id}</td>')
            result.append(f'<td>{flat.address}</td>')
            result.append(f'<td>{flat.price} ₽</td>')
            result.append(f'<td>{flat.town}</td>')
            result.append(f'</tr>')

        result.append('</table>')
        return ''.join(result)

    flats_list.short_description = 'Список квартир'
    flats_list.allow_tags = True

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('flats')