from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe

from accounts.models import Laboratory, LaboratoryMembership, Profile, User

IMAGE_TAG = (
    '<img src="{url}" width="150" height="150" alt="Preview unavailable!" />'
)


class LaboratoryMembershipInLine(admin.TabularInline):
    model = LaboratoryMembership
    extra = 0


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    fields = "title", "image", "image_tag", "date_of_birth", "institute", "bio"
    readonly_fields = ("image_tag",)

    def image_tag(self, instance: Profile) -> str:
        html = IMAGE_TAG.format(url=instance.image.url)
        return mark_safe(html)

    image_tag.short_description = "Preview"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, LaboratoryMembershipInLine)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "get_institute",
        "is_staff",
        "is_superuser",
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
    list_display = (
        "id",
        "title",
        "description",
        "created",
        "modified",
        "n_members",
    )
    inlines = (LaboratoryMembershipInLine,)
    fields = "title", "description", "image", "image_tag"
    readonly_fields = ("image_tag", "n_members")

    class Media:
        css = {"all": ("accounts/css/hide_admin_original.css",)}

    def image_tag(self, instance: Laboratory) -> str:
        html = IMAGE_TAG.format(url=instance.image.url)
        return mark_safe(html)

    def n_members(self, instance: Laboratory) -> int:
        return instance.members.count()

    image_tag.short_description = "Preview"
    n_members.short_description = "# members"


admin.site.register(User, UserAdmin)
admin.site.register(Laboratory, LaboratoryAdmin)
