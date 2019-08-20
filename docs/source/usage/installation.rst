Installation
=============

1. Clone *pylabber* to a local directory::

    git clone https://github.com/ZviBaratz/pylabber.git


2. From within the project's directory, create a virtual environment using `venv <https://docs.python.org/3/library/venv.html>`_::

    python3.6 -m venv venv


3. Activate the virtual environment by typing::

    . venv/bin/activate


4. If you intend on using *pylabber* along with the `django_mri <https://github.com/ZviBaratz/django_mri>`_
extension to manage MRI data, you must first:

    * Clone both `django_mri <https://github.com/ZviBaratz/django_mri>`_ and `django_dicom <https://github.com/ZviBaratz/django_dicom>`_.
    * Install each package locally within the *pylabber* virtual environment using::

        pip install -e [LOCAL PATH]

Otherwise, delete these packages from Django's *settings.py*
`INSTALLED_APPS <https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-INSTALLED_APPS>`_
definition.


5. Install the required dependencies::

    pip install -r requirements/common.txt

If you need the development dependencies, you may call `requirements/dev.txt`
instead.


6. Make sure you have `PostgreSQL installed <https://wiki.postgresql.org/wiki/Detailed_installation_guides>`_
and create a database to be used by the project.

.. seealso:: The are many tutorials online that explain this process in detail, some recommended ones can be found in `DigitalOcean <https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04>`_, `DjangoGirls <https://tutorial-extensions.djangogirls.org/en/optional_postgresql_installation/>`_, `Medium <https://medium.com/agatha-codes/painless-postgresql-django-d4f03364989>`_, and more.


7. Create the appropriate environment variables for the *settings.py* file. You
can find each of those variables wrapped in an *env("VAR_NAME")* call.

An example for an environment variables definition in development could look like ::

    export ALLOWED_HOSTS=*
    export DEBUG=true
    export SECRET_KEY="s0m3-$\/pER-s3CrE7_kEy!"
    export DB_NAME=pylabber
    export DB_USER=postgres
    export DB_PASSWORD=p$q1@ddmmIN
    export MEDIA_ROOT="/where/to/save/files/locally/"

.. seealso:: For more information about Django settings see the `Django documentation <https://docs.djangoproject.com/en/2.2/ref/settings/>`_.


8. Create and apply the required Django migrations::

    ./manage.py makemigrations
    ./manage.py migrate


9. Run *pylabber* locally::

    ./manage.py runserver

