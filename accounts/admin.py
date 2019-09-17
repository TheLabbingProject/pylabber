from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import LaboratoryMembership, Laboratory, Profile, User


class LaboratoryMembershipInLine(admin.TabularInline):
    model = LaboratoryMembership
    extra = 1


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, LaboratoryMembershipInLine)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "get_institute",
        "is_staff",
    )
    list_select_related = ("profile",)

    def get_institute(self, instance):
        return instance.profile.institute

    get_institute.short_description = "Institute"

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "created", "modified")
    inlines = (LaboratoryMembershipInLine,)


admin.site.register(User, UserAdmin)
admin.site.register(Laboratory, LaboratoryAdmin)
