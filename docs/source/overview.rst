Overview
========

*pylabber* is a collaborative open-source project meant to facilitate research.

This `Django <https://www.djangoproject.com>`_ 
`project <https://docs.djangoproject.com/en/2.2/glossary/#term-project>`_ 
provides the infrastructure for scientific work, and is built and maintained to 
be as flexible and as extendible as possible.

Currently, the project hosts two `apps <https://docs.djangoproject.com/en/2.2/ref/applications/>`_;
*accounts* and *research*.

- *accounts* manages users (researchers) and labs.
- *research* manages studies, study groups, and subjects.


This architecture is meant to be as abstract as possible, in order to allow for
it to easily lend itself to a wide variety of research disciplines.

*pylabber* provides a `RESTful API <https://en.wikipedia.org/wiki/Representational_state_transfer>`_
that may be adapted and integrated into your own field of research.
