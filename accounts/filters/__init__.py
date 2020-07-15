"""
Filters for :ref:`the app's models <modules/accounts.models:accounts.models
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

from accounts.filters.user import UserFilter
