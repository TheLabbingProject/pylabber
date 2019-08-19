from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination parameters definition. This didn't seem to work
    when implemented as part of the defaults mixin and therefore was moved
    to this class, which is meant to be set in the
    `ViewSets <https://www.django-rest-framework.org/api-guide/viewsets/>`_'
    *pagination_class* attribue definition, or in the REST_FRAMEWORK definition
    within settings.py. For much information see
    `the DRF documentation <https://www.django-rest-framework.org/api-guide/pagination/#modifying-the-pagination-style>`_.
    
    """

    page_size = 25
    page_size_query_param = "page_size"
