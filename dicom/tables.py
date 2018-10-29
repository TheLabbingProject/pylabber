import django_tables2 as tables
from .models import SMBFile


class SMBFileTable(tables.Table):
    class Meta:
        model = SMBFile
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'id',
            'path',
            'source',
            'is_archived',
            'is_available',
        )
        attrs = {"class": "table table-striped table-hover table-sm"}
        empty_text = "There are no files matching the search criteria..."
