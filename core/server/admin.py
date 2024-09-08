from django.contrib import admin
from .models import InfoSource

@admin.register(InfoSource)
class InfoSourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    search_fields = ('title', 'tags')
    list_filter = ('category',)
