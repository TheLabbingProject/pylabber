from .models import Study


class StudyListMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["studies"] = Study.objects.all()
        return context
