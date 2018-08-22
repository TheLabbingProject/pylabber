import django_filters
from .models import Subject


class SubjectListFilter(django_filters.FilterSet):
    class Meta:
        model = Subject
        fields = [
            'id',
            'first_name',
            'last_name',
            'sex',
            'gender',
            'date_of_birth',
            'id_number',
        ]
