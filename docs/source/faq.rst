Frequently Asked Questions
==========================

.. contents:: :local:
    :depth: 1

What is The Labbing Project?
----------------------------

A collection of reusable Django apps and a single dedicated parent Django
project (i.e. pylabber) used to manage and share research data and derivatives
across researchers and across labs.

.. hint::

    For more information about the difference between
    Django apps and projects, see Django's `Projects and Applications`_
    documentation.

Is The Labbing Project only suitable for MRI-based neuroscientific research?
----------------------------------------------------------------------------

Not at all! The purpose of the :mod:`research` app is to provide common,
generic models (such as :class:`~research.models.subject.Subject` and
:class:`~research.models.study.Study`) that may be associated with any number of
data models originating from any number of reusable apps.

How are different data types integrated into the application's database?
------------------------------------------------------------------------

The modular design of the project enables researchers from different fields
to create specialized apps that manage the relevant data formats and
facilitate commonplace workflows. E.g. the first app created for this purpose
was `django_dicom`_, which manages `DICOM`_ data, and the second was
`django_mri`_, providing a format-agnostic
:class:`~django_mri.models.scan.Scan` abstraction, as well as other useful
models and MRI-based research utilities. Each reusable app integrates with
pylabber's internal :mod:`research` app to associate the data with an
instance of the :class:`~research.models.subject.Subject` model. For
more information, see pylabber's `overview`_.

.. _django_dicom:
   https://github.com/TheLabbingProject/django_dicom
.. _django_mri:
   https://github.com/TheLabbingProject/django_mri
.. _DICOM:
   https://dicom.nema.org/
.. _overview:
   https://pylabber.readthedocs.io/en/latest/overview.html#overview
.. _Projects and Applications:
   https://docs.djangoproject.com/en/3.1/ref/applications/#projects-and-applications