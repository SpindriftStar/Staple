from django.contrib import admin

from .models import Host, Interface, Auth, Template, Instance

class HostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'manufacturer', 'model', 'series', 'status', 'create_time', 'config']
    list_per_page = 15
    search_fields = ['name', 'manufacturer', 'status']
    list_display_links = ['id', 'name', 'config']
    ordering = ['create_time']
    readonly_fields = ['manufacturer', 'model', 'series', 'create_time']
    fields = ['name', 'manufacturer', 'model', 'series', 'status', 'create_time', 'config']
    
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'host_id', 'ip', 'port', 'status']
    list_per_page = 15
    search_fields = ['host_id', 'ip']
    list_display_links = ['id', 'description']
    ordering = ['id', 'host_id']
    #readonly_fields = ['host_id']
    fields = ['description', 'host_id', 'ip', 'port', 'status']
    
class AuthAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'host_id']
    list_per_page = 15
    search_fields = ['username', 'host_id']
    list_display_links = ['id', 'username']
    ordering = ['id', 'host_id']
    readonly_fields = ['host_id', 'password']
    exclude = ['password']
    fields = ['username', 'password', 'host_id']

admin.site.register(Host, HostAdmin)
admin.site.register(Interface, InterfaceAdmin)