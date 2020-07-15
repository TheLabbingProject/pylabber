"""
Filters for :ref:`the app's models <modules/research.models:research.models
package>`.

See Also
--------

    * `Django REST Framework`_ `filtering documentation`_.
    * django-filter_'s documentation for `Integration with DRF`_.

.. _django-filter: https://django-filter.readthedocs.io/en/stable/index.html
.. _Django REST Framework: https://www.django-rest-framework.org/
.. _filtering documentation:
   https://www.django-rest-framework.org/api-guide/filtering/
.. _Integration with DRF:
   https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html
"""

from research.filters.subject_filter import SubjectFilter
from research.filters.group_filter import GroupFilter
