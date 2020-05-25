[![Join the chat at https://gitter.im/pylabber/community](https://badges.gitter.im/pylabber/community.svg)](https://gitter.im/pylabber/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![PyPI version](https://img.shields.io/pypi/v/pylabber.svg)](https://pypi.python.org/pypi/pylabber/)
[![PyPI status](https://img.shields.io/pypi/status/pylabber.svg)](https://pypi.python.org/pypi/pylabber/)
[![TheLabbingProject](https://circleci.com/gh/TheLabbingProject/pylabber.svg?style=shield)](https://app.circleci.com/pipelines/github/TheLabbingProject/pylabber)

# _pylabber_

## Overview

_pylabber_ is a collaborative open-source initiative meant to facilitate research.

This repository hosts the [Django](https://www.djangoproject.com/) [project](https://docs.djangoproject.com/en/2.2/glossary/#term-project) providing the infrastructure for domain-specific [reusable](https://docs.djangoproject.com/en/3.0/intro/reusable-apps/#reusability-matters) Django [apps](https://docs.djangoproject.com/en/2.2/ref/applications/). Integration is generally achieved through _pylabber_'s own:

- _accounts_ - Manages users (researchers) and labs.
- _research_ - Manages studies, study groups, and subjects.

## Data Integration

_pylabber_ is extended by:

- [_django_mri_](https://github.com/TheLabbingProject/django_mri) - Format agnostic tools to manage and analyze MRI data.
- [_django_analyses_](https://github.com/TheLabbingProject/django_analyses) - A database-supported pipeline engine.

## Front-end

For a front-end project built on top of _pylabber_, see [vuelabber](https://github.com/TheLabbingProject/vuelabber).

## Docker

In order to set-up pylabber quickly and easily using [Docker](https://www.docker.com/), simply run:

```
docker-compose up --build -d
```

within the project's root directory.

You will then have a running container exposed on port 8000. In order to connect to the admin interface visit: `https://localhost:8000/admin` and sign-in as with "admin" as the username and password.
