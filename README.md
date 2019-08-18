# pylabber

[![Join the chat at https://gitter.im/pylabber/community](https://badges.gitter.im/pylabber/community.svg)](https://gitter.im/pylabber/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

_pylabber_ is a collaborative open-source project meant to facilitate research.

This [Django](https://www.djangoproject.com/) [project](https://docs.djangoproject.com/en/2.2/glossary/#term-project)
provides the infrastructure for scientific work, and is built and maintained to be
as flexible and as extendible as possible.

Currently, the project hosts two [apps](https://docs.djangoproject.com/en/2.2/ref/applications/);
_accounts_ and _research_.

- _accounts_ manages users (researchers) and labs.
- _research_ manages studies, study groups, and subjects.

This general structure is meant to be as abstract as possible, in order to allow
for it to easily lend itself to a wide variety of research disciplines. The product
of this is a RESTful API that may be adapted and integrated into your own field
of research.

Currently, existing packages that integrate into this project are:

- [_django_dicom_](https://github.com/ZviBaratz/django_dicom) - provides a
  the tools to easily parse, store, and query MRI data in the DICOM format.
- [_django_mri_](https://github.com/ZviBaratz/django_mri) - provides an abstraction
  over _django_dicom_ in order to provide format agnostic toosl to manage and interact
  with MRI data.

For a frontend project built on top of _pylabber_, see [vuelabber](https://github.com/ZviBaratz/vuelabber).
