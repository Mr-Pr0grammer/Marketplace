from django.contrib import admin
from .models import UserComplaint


class UserComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'sent_at')
    list_display_links = ('user',)
    list_per_page = 50
    search_fields = ('user',)
    search_help_text = 'Enter username'


admin.site.register(UserComplaint, UserComplaintAdmin)