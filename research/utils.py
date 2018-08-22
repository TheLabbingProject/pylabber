from django_tables2 import SingleTableMixin
from django_filters.views import FilterView


class FilteredTableMixin(SingleTableMixin, FilterView):
    formhelper_class = None
    filterset_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset().order_by('-id')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context[self.context_filter_name] = self.filter
        return context
