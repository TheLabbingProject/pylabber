Welcome to pylabber's documentation!
======================================

*pylabber* is a Django_ project designed to provide the core functionality
required to conduct neuroscientific research.

.. seealso::
   For more information about Django applications and the difference between
   projects and apps see the documentation's `getting started`_ page, as well
   as the `projects and applications`_ section.

   .. _getting started:
      https://docs.djangoproject.com/en/3.0/intro/
   .. _projects and applications:
      https://docs.djangoproject.com/en/3.0/ref/applications/#projects-and-applications

The project's root directory contains the :mod:`pylabber` module, which holds
the applications settings and `URL configurations`_, as well as two native
apps:

   * :mod:`~accounts`: Manages user (i.e. researcher) accounts.
   * :mod:`~research`: Manages the most elementary "research entities";
     :class:`~research.models.subject.Subject`,
     :class:`~research.models.study.Study`, and
     :class:`~research.models.group.Group`.

.. _Django:
   https://www.djangoproject.com/
.. _URL configurations:
   https://docs.djangoproject.com/en/3.0/topics/http/urls/

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   usage/installation
   modules/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
