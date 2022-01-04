from django.contrib import admin
from .models import BloodTest


@admin.register(BloodTest)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'submit', 'client_ip', 'parsing_completed')
    list_filter = ('parsing_completed',)
    search_fields = ('id', 'client_ip', 'client_file')
    date_hierarchy = 'submit'
    ordering = ('id', 'submit')
