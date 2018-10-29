import django_filters
from .models import SMBDirectory, SMBFile


class SMBFileListFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label='#')
    path = django_filters.CharFilter(
        label='Path',
        lookup_expr='icontains',
    )
    source = django_filters.ModelMultipleChoiceFilter(
        label='Data Source',
        queryset=SMBDirectory.objects.all(),
    )
    is_archived = django_filters.BooleanFilter(label='Archived')

    class Meta:
        model = SMBFile
        fields = [
            'id',
            'path',
            'source',
            'is_archived',
        ]
