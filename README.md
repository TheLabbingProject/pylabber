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

- [_django_mri_](https://github.com/ZviBaratz/django_mri) - an abstraction over [_django_dicom_](https://github.com/ZviBaratz/django_dicom) meant to provide format agnostic tools to manage and interact with MRI data.

## Front-end

For a front-end project built on top of _pylabber_, see [vuelabber](https://github.com/ZviBaratz/vuelabber).

## About

The purpose of _pylabber_ is to give researchers the power to manage and share their data in an open and easy manner. No more hard-drives with valuable data forgotten in random laboratories' drawers, no more in-house, untested and unmaintained scripts to inefficiently query your data, stored locally in some makeshift directory structure. It is meant to give a unified and community-based solution for all of the vacuous technical work researchers often have to overcome instead of doing **research**.
