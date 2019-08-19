# _pylabber_

[![Join the chat at https://gitter.im/pylabber/community](https://badges.gitter.im/pylabber/community.svg)](https://gitter.im/pylabber/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Overview

_pylabber_ is a collaborative open-source project meant to facilitate research.

This [Django](https://www.djangoproject.com/) [project](https://docs.djangoproject.com/en/2.2/glossary/#term-project) provides the infrastructure for scientific work, and is built and maintained to be as flexible and as extendible as possible.

Currently, the project hosts two [apps](https://docs.djangoproject.com/en/2.2/ref/applications/);
_accounts_ and _research_.

- _accounts_ manages users (researchers) and labs.
- _research_ manages studies, study groups, and subjects.

This architecture is meant to be as abstract as possible, in order to allow for it to easily lend itself to a wide variety of research disciplines.

_pylabber_ provides a [RESTful API](https://en.wikipedia.org/wiki/Representational_state_transfer) that may be adapted and integrated into your own field of research.

## Data Integration

Currently, _pylabber_ has only one available extension:

- [_django_mri_](https://github.com/ZviBaratz/django_mri) - provides an abstraction over [_django_dicom_](https://github.com/ZviBaratz/django_dicom) in order to provide format agnostic tools to manage and interact with MRI data.

## Front-end

For a frontend project built on top of _pylabber_, see [vuelabber](https://github.com/ZviBaratz/vuelabber).
