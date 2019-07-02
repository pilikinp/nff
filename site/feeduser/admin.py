from django.contrib import admin

from feeduser.models import FeedUser, ProducerProfile


class FeedUserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'birth_date',
        'age'
    ]

    fieldsets = (
        (
            'account', {'fields': ('username',)}
        ),
        (
            'name', {'fields': ('first_name', 'last_name',)}
        ),
        (
            'contacts', {'fields': ('email',)}
        ),
        (
            'info', {'fields': ('birth_date',)}
        )
    )

    def age(self, obj):
        return obj.age


class ProducerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'birth_date',
        'age'
    ]

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def birth_date(self, obj):
        return obj.user.birth_date

    def age(self, obj):
        return obj.user.age


admin.site.register(FeedUser, FeedUserAdmin)
admin.site.register(ProducerProfile, ProducerProfileAdmin)
