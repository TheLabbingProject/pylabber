from django_filters.rest_framework import DjangoFilterBackend
from research.models.group import Group
from research.models.study import Study
from research.models.subject import Subject
from research.serializers.study_serializer import StudySerializer
from research.serializers.subject_serializer import SubjectSerializer
from research.serializers.group_serializer import GroupSerializer, GroupReadSerializer
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated


class DefaultsMixin:
    """
    Default settings for view authentication, permissions, filtering and pagination.
    
    """

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    paginate_by = 25
    paginate_by_param = "page_size"
    max_paginate_by = 100
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)


class StudyViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows studies to be viewed or edited.
    
    """

    queryset = Study.objects.all()
    serializer_class = StudySerializer


class SubjectViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows subjects to be viewed or edited.
    
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class GroupViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows study groups to be viewed or edited.
    
    """

    queryset = Group.objects.all()
    # serializer_class = GroupSerializer
    filter_fields = ("study__id", "study__title")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GroupReadSerializer
        return GroupSerializer


# Old views:

# class StudyListView(LoginRequiredMixin, ListView):
#     model = Study
#     template_name = "research/studies/study_list.html"
#     context_object_name = "studies"


# class StudyCreateView(LoginRequiredMixin, StudyListMixin, CreateView):
#     model = Study
#     template_name = "research/studies/study_create.html"
#     fields = ["title", "description", "collaborators"]
#     success_url = reverse_lazy("research:study_list")


# def parse_lazy_pk(request) -> int:
#     value = request.get_full_path().split("=")[-1]
#     try:
#         return int(value)
#     except ValueError:
#         return 0


# def generate_study_mri_json(request):
#     if request.method == "GET":
#         pk = parse_lazy_pk(request)
#         study = get_object_or_404(Study, pk=pk)
#         data = study.generate_dicom_tree()
#         return JsonResponse(data, safe=False)
#     else:
#         return HttpResponse("Request method must be GET!")


# class StudyDetailView(LoginRequiredMixin, StudyListMixin, DetailView):
#     model = Study
#     template_name = "research/studies/study_detail.html"


# class StudySubjectDetailView(LoginRequiredMixin, StudyListMixin, DetailView):
#     model = Study
#     template_name = "research/subjects/subject_study_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pk = parse_lazy_pk(self.request)
#         subject = Subject.objects.get(id=pk)
#         context["subject"] = subject
#         return context


# def embeddable_subject_view(request, study_id: int, subject_id: int):
#     subject = get_object_or_404(Subject, pk=subject_id)
#     return render(
#         request, "research/subjects/subject_study_detail.html", {"subject": subject}
#     )


# class StudyUpdateView(LoginRequiredMixin, StudyListMixin, UpdateView):
#     model = Study
#     fields = ["title", "description", "collaborators"]
#     template_name = "research/studies/study_update.html"


# class StudyDeleteView(LoginRequiredMixin, StudyListMixin, DeleteView):
#     model = Study
#     template_name = "research/studies/study_delete.html"
#     success_url = reverse_lazy("research:study_list")


# class SubjectListView(LoginRequiredMixin, FilteredTableMixin):
#     model = Subject
#     table_class = SubjectTable
#     template_name = "research/subjects/subject_list.html"
#     paginate_by = 50
#     ordering = ["-id"]
#     filterset_class = SubjectListFilter
#     formhelper_class = SubjectListFormHelper

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         search_query = self.get_queryset()
#         table = self.table_class(search_query)
#         RequestConfig(self.request).configure(table)
#         context["table"] = table
#         return context


# class SubjectDetailView(SubjectListView):
#     model = Subject
#     template_name = "research/subjects/subject_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         subject = Subject.objects.get(id=self.kwargs.get("pk"))
#         context["subject"] = subject
#         return context


# class SubjectUpdateView(SubjectListView, UpdateView):
#     model = Subject
#     fields = [
#         "id_number",
#         "first_name",
#         "last_name",
#         "sex",
#         "gender",
#         "date_of_birth",
#         "dominant_hand",
#     ]
#     template_name = "research/subjects/subject_update.html"

#     def get_context_data(self, **kwargs):
#         subject = Subject.objects.get(id=self.kwargs["pk"])
#         self.object = subject
#         context = super().get_context_data(**kwargs)
#         context["subject"] = subject
#         return context


# class SubjectDeleteView(SubjectListView, DeleteView):
#     model = Subject
#     template_name = "research/subjects/subject_delete.html"
#     success_url = reverse_lazy("research:subject_list")

#     def get_context_data(self, **kwargs):
#         subject = Subject.objects.get(id=self.kwargs["pk"])
#         self.object = subject
#         context = super().get_context_data(**kwargs)
#         context["subject"] = subject
#         return context


# class SubjectCreateView(LoginRequiredMixin, CreateView):
#     model = Subject
#     template_name = "research/subjects/subject_create.html"
#     fields = [
#         "id_number",
#         "first_name",
#         "last_name",
#         "sex",
#         "gender",
#         "date_of_birth",
#         "dominant_hand",
#     ]


## If in the future we need to use SMB:

# def import_dcms_from_node(node: RemotePath):
#     try:
#         for descendant in node.get_descendants():
#             if descendant.name.endswith(".dcm") and not descendant.is_imported:
#                 f = descendant.get_file()
#                 Image.objects.from_dcm(f)
#                 descendant.is_imported = True
#                 descendant.save()
#         return True
#     except Exception as e:
#         print(e)
#         return False


# def import_node(request):
#     if request.method == "GET":
#         request_path = request.get_full_path()
#         path_id = request_path.split("=")[-1]
#         node = RemotePath.objects.get(id=path_id)
#         result = import_dcms_from_node(node)
#         if result:
#             return HttpResponse(node.id)
#         return HttpResponse(f"Failure")
#     else:
#         return HttpResponse("Request method must be GET!")
