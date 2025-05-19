from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Core, Contact


MAX_OBJECTS = 1
admin.site.site_title = _('پیشخوان')
admin.site.site_header = _('پیشخوان')
# admin.site.index_title = _('')

@admin.register(Core)
class CoreAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'phone', 'mobile', 'email', 'created', 'updated']
    fields = [
        ('title', 'subtitle'), ('phone', 'mobile'), 'email',
        ('logo', 'favicon'), 'about', 'contact',
    ]

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'created', 'updated']
    list_editable = ['status']
    list_filter = ['status']
