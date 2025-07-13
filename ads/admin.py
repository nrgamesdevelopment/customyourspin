from django.contrib import admin
from django.utils.html import format_html
from .models import Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('ad_name', 'display_image', 'link', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('ad_name', 'link')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Ad Information', {
            'fields': ('ad_name', 'link')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Image Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
