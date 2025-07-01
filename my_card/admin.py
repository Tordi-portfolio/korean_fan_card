from django.contrib import admin
from .models import UserCard
from django.utils.html import format_html

@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'text_preview', 'image_preview', 'uploaded_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "(No image)"
    image_preview.short_description = 'Image'

    def text_preview(self, obj):
        return obj.text[:30] + "..." if len(obj.text) > 30 else obj.text
    text_preview.short_description = 'Text'
