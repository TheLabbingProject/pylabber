import django_tables2 as tables
from django_tables2.utils import A
from .models import Subject


class SubjectTable(tables.Table):
    id = tables.LinkColumn('subject_detail', args=[A('pk')])

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
