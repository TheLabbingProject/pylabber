import django_tables2 as tables

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django_tables2.utils import A, AttributeDict
# from django_smb.models import RemoteFile
from research.models import Subject


class SubjectTable(tables.Table):
    id = tables.LinkColumn('research:subject_detail', args=[A('pk')])

    class Meta:
        model = Subject
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'id',
            'first_name',
            'last_name',
            'sex',
            'date_of_birth',
            'id_number',
        )
        attrs = {"class": "table table-striped table-hover table-sm"}
        empty_text = "There are no subjects matching the search criteria..."


class BooleanCircleColumn(tables.BooleanColumn):
    def render(self, value):
        value = bool(value)
        text = self.yesno[int(not value)]
        html = '<span {}>{}</span>'
        class_name = 'fas fa-circle'
        if value:
            style = 'color: green;'
        else:
            style = 'color: red;'
        attrs = {'class': class_name, 'style': style}
        attrs.update(self.attrs.get('span', {}))
        return mark_safe(
            html.format(AttributeDict(attrs).as_html(), escape(text)))


class StylizedBooleanColumn(tables.BooleanColumn):
    def render(self, value):
        value = bool(value)
        text = self.yesno[int(not value)]
        html = '<span {}>{}</span>'
        if value:
            style = 'color: green;'
        else:
            style = 'color: red;'
        attrs = {'style': style}
        attrs.update(self.attrs.get('span', {}))
        return mark_safe(
            html.format(AttributeDict(attrs).as_html(), escape(text)))


# class SMBRemoteFileTable(tables.Table):
#     is_archived = StylizedBooleanColumn()
#     is_available = BooleanCircleColumn(yesno=',')

#     class Meta:
#         model = RemoteFile
#         template_name = 'django_tables2/bootstrap.html'
#         fields = (
#             'id',
#             'path',
#             'source',
#             'is_archived',
#             'is_available',
#         )
#         attrs = {"class": "table table-striped table-hover table-sm"}
#         empty_text = "There are no files matching the search criteria..."
