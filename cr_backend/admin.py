from django.contrib import admin

from .models import ChangeRequest, ChangeRequestLog, Ministry, Role, System


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    search_fields = ('name', 'group__name')


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'ministry')
    list_filter = ('ministry',)
    search_fields = ('name',)
    filter_horizontal = ('owners',)


class ChangeRequestLogInline(admin.TabularInline):
    model = ChangeRequestLog
    extra = 0
    readonly_fields = ('action', 'performed_by', 'timestamp')
    can_delete = False


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'system', 'ministry', 'change_category', 'created_by', 'created_at')
    list_filter = ('status', 'system', 'ministry', 'change_category', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = (ChangeRequestLogInline,)


@admin.register(ChangeRequestLog)
class ChangeRequestLogAdmin(admin.ModelAdmin):
    list_display = ('change_request', 'action', 'performed_by', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('change_request__title', 'performed_by__username')
    readonly_fields = ('change_request', 'action', 'performed_by', 'timestamp')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
