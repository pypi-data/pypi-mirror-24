from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import Client, ReleaseNote


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'itunes_url',
        'created', 'modified',
    )


@admin.register(ReleaseNote)
class ReleaseNoteAdmin(admin.ModelAdmin):
    list_display = (
        'notes', 'release_date', 'is_published', 'client',
        'created', 'modified',
    )
