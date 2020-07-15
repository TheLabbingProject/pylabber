Installation
=============

.. note::
    *pylabber* requires PostgreSQL. Before starting the installation, make sure
    you have PostgreSQL_ installed_ and create a new database.

    .. _installed:
       https://wiki.postgresql.org/wiki/Detailed_installation_guides
    .. _PostgreSQL:
       https://www.postgresql.org/

    There are many tutorials online providing detailed instructions on how to
    do this, some recommended ones can be found in `Digital Ocean`_,
    DjangoGirls_, and Medium_.

    .. _Digital Ocean:
        https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
    .. _DjangoGirls:
        https://tutorial-extensions.djangogirls.org/en/optional_postgresql_installation/
    .. _Medium:
        https://medium.com/agatha-codes/painless-postgresql-django-d4f03364989


1. Clone *pylabber* to a local directory:

    .. code-block:: console

        $ git clone https://github.com/TheLabbingProject/pylabber

2. From within the project's directory, create a virtual environment using
   venv_:

    .. code-block:: console

        $ python3 -m venv venv

3. Activate the virtual environment:

    .. code-block:: console

        $ source venv/bin/activate

4. Install the required dependencies:

    .. code-block:: console

        $ pip install -r requirements.txt

5. Create the appropriate environment variables for the *settings.py* file. You
can find each of those variables wrapped in an *env("VAR_NAME")* call.

An example for an environment variables definition in development could look like:

.. code-block:: sh
    :caption: .env

    export SECRET_KEY="s0m3-$\/pER-s3CrE7_kEy!"
    export DB_NAME=pylabber
    export DB_USER=postgres
    export DB_PASSWORD=p$q1@ddmmIN
    export MEDIA_ROOT="/where/to/save/files/locally/"

6. Apply the project's migrations_:

    .. code-block:: console

        $ python manage.py migrate



7. Run *pylabber* locally:

    .. code-block:: console

        $ python manage.py runserver

   or, open an interactive `Django shell`_ using `django-extensions`_:

   .. code-block:: console

       $ python manage.py shell_plus


.. _django-extensions:
   https://django-extensions.readthedocs.io/en/latest/
.. _Django shell:
    https://docs.djangoproject.com/en/3.0/ref/django-admin/#shell
.. _migrations:
    https://docs.djangoproject.com/en/3.0/topics/migrations/
.. _venv:
    https://docs.python.org/3/library/venv.html