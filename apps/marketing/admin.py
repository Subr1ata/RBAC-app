from django.contrib import admin
from .models import Marketing

@admin.register(Marketing)
class MarketingAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
