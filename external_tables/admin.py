from django.contrib import admin

from external_tables.models.google_sheet import GoogleSheet


class GoogleSheetAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~external_tables.models.google_sheet.GoogleSheet` class to
    the admin interface.
    """

    list_display = (
        "key",
        "sheet_name",
        "content_type",
        "id_column",
        "id_field",
    )


admin.site.register(GoogleSheet, GoogleSheetAdmin)
