"""
`Django REST Framework <https://www.django-rest-framework.org/>`_
`ViewSets <https://www.django-rest-framework.org/api-guide/viewsets/>`_
for the :mod:`accounts` package.

"""

from accounts.views.group import GroupViewSet
from accounts.views.laboratory import LaboratoryViewSet
from accounts.views.profile import ProfileViewSet
from accounts.views.user import UserViewSet
