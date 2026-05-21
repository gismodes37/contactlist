from django.contrib import admin

from contacts.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'birth', 'created')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created', 'birth')
    date_hierarchy = 'created'
    ordering = ('-created',)