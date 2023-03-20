================================================================================
  Docker Compose DativeBase Deploy Locally with HTTP
================================================================================

This document provides help on deploying DativeBase locally on HTTP.

For an example of deploying DativeBase locally on HTTPS, see the ``README`` under
the sister directory ``docker-compose/``.

.. contents::


Summary
================================================================================

Run the following commands if they make sense to you. Otherwise, follow the more
detailed instructions below.::

  $ git clone https://github.com/dativebase/dativebase.git
  $ cd dativebase
  $ git submodule update --init --recursive
  $ cd docker-compose-http
  $ make create-volumes
  $ docker-compose up -d --build
  $ make bootstrap
  $ make restart-dativebase-services

- Dative: http://localhost:61000/dative/
- OLD instance: http://localhost:61000/olds/old


Audience
================================================================================

This DativeBase environment is based on `Docker Compose`_ and is specifically
designed to make it easy for **developers** to quickly and reliably deploy
`Dative`_ and the `Online Linguistic Database`_ in a local development
environment. Compose can be used in a production environment but that is beyond
the scope of this recipe.


Requirements
================================================================================

Docker, Docker Compose, git and make.

It is beyond the scope of this document to explain how these dependencies are
installed in your computer. If you are using Ubuntu 16.04 the following commands
may work::

  $ sudo apt update
  $ sudo apt install -y build-essential python-dev git
  $ sudo pip install -U docker-compose

Install Docker Community Edition (CE) following `these instructions`_.


Docker and Linux
--------------------------------------------------------------------------------

To use Docker on Linux as a non-root user, add your user to the ``docker`` group
with something like::

  $ sudo usermod -aG docker <user>

Remember that you will have to log out and back in for this to take effect.

.. warning:: Adding a user to the ``docker`` group will grant the ability to run
   containers which can be used to obtain root privileges on the docker host.
   Refer to `docker daemon attack surface`_ for more information.


.. _installation:

Installation
================================================================================


Download the Source
--------------------------------------------------------------------------------

First clone the source and move into the directory created::

  $ git clone https://github.com/dativebase/dativebase.git
  $ cd dativebase

Then clone the Dative and OLD submodules under ``src/``::

  $ git submodule update --init --recursive


Bring up the DativeBase Docker Containers
--------------------------------------------------------------------------------

Now create a Docker volume shared with your host machine at
``/tmp/dativebase-old-store/`` so that you can view your uploaded OLD files
(e.g., audio recordings) at that directory::

  $ cd docker-compose-http
  $ make create-volumes

Build the Docker containers running Dative, the OLD, MySQL and Nginx (see
``docker-compose/docker-compose.yml`` for the specific configuration of these
services)::

  $ docker-compose up -d --build

Initialize a new OLD instance named "old". This means creating a MySQL database
named ``old`` running in the ``mysql`` container that has all of the OLD table
schemas defined within it. This also means creating the directory structure to
hold the audio (and other) files for this OLD; see
``/tmp/dativebase-old-store/old/``::

  $ make bootstrap

Now restart the services::

  $ make restart-dativebase-services

If all goes well, the above should result in Dative and an OLD instance being
served at the following HTTP URLs:

- Dative:       http://localhost:61000/dative/
- OLD instance: http://localhost:61000/olds/old

If you navigate to the Dative URL in a browser, you should see the Dative app.

If you navigate to the OLD forms URL (or issue a ``curl`` ``GET`` request to it)
http://localhost:61000/olds/old/forms, you should see the following because you
are not yet authenticated::

  {"error":"Authentication is required to access this resource."}

To login to your old instance from Dative, navigate to Dative at
http://localhost:61000/dative/, click on Dative, then Application Settings, then
click on the *Servers* button, and create a server with URL value
``http://localhost:61000/olds/old`` and a name like ``Local OLD``. Now you
should be able to sign in to this OLD instance by clicking on the lock icon in
the top right, selecting ``Local OLD`` as the server value and entering username
``admin`` and password ``adminA_1``.


GNU make
--------------------------------------------------------------------------------

The documentation for the ``docker-compose/Makefile`` can be viewed by calling
``make help`` or just ``make``::

  $ pwd
  dativebase/docker-compose-http
  $ make help


Create OLD Instances
--------------------------------------------------------------------------------

An OLD instance is identified by its name. Its state (user data) is stored as a
MySQL database of the same name and a directory in
``/tmp/dativebase-old-store/`` of the same name. To create a new OLD instance,
e.g., with name ``old2``::

  $ make create-old-instance OLD_NAME=old2

If the above worked, you will see the following directory on your local machine::

  $ ls /tmp/dativebase-old-store/old2


Source code auto-reloading
================================================================================

The source code for Dative and the OLD is at ``../src/dative/`` and
``../src/old/,`` respectively.

The OLD is served by pserve and Waitress. We set up pserve with the `reload`_
setting enabled, meaning that the Waitress server will be restarted as soon as
code changes.

Dative does not currently automatically reload when its source code is changed.
This is due to some unanticipated issue with grunt's auto-reloading and Docker.

To manually restart a component (in this case Dative)::

    $ docker-compose up -d --force-recreate --no-deps dative

If you have added new dependencies or changes to the ``Dockerfile`` you should
also add the ``--build`` argument to the previous command in order to ensure
that the container is using the newest image, e.g.::

    $ docker-compose up -d --force-recreate --build --no-deps old


Logs
================================================================================

The logs of all component processes are (or should be) sent to stdout. This
makes it easier to aggregate the logs generated by all of the replicas that we
may be deploying of our services across the cluster.

Docker Compose aggregates the logs for us so you can see everything from one
place. Some examples::

    $ docker-compose logs -f
    $ docker-compose logs -f old
    $ docker-compose logs -f nginx old


Scaling
================================================================================

With Docker Compose we can run as many containers as we want for a service,
e.g. by default we only provision a single replica of the ``OLD`` service but
we could run more::

    $ docker-compose up -d --scale old=3

This would give us one service but three containers.


Ports
================================================================================

+-----------------------------------------+----------------+---------------+
| Service                                 | Container port | Host port     |
+=========================================+================+===============+
| nginx > Dative & OLD                    | ``tcp/80``     | ``tcp/61000`` |
+-----------------------------------------+----------------+---------------+
| OLD                                     | ``tcp/8000``   | ``tcp/61081`` |
+-----------------------------------------+----------------+---------------+
| Dative                                  | ``tcp/9000``   | ``tcp/61080`` |
+-----------------------------------------+----------------+---------------+
| mysql                                   | ``tcp/3306``   | ``tcp/61002`` |
+-----------------------------------------+----------------+---------------+


Tests
================================================================================

To run the OLD tests::

    $ make test-old

To run specific OLD tests, in this example those in the ``test_multiple_olds``
module::

    $ part=old/tests/functional/test_multiple_olds.py make test-old-part


Resetting the Environment
================================================================================

In many cases, as a tester or a developer, you will want to restart all of the
containers at once in order to make sure that the latest version of the images
are built. However, you will also want to avoid losing your data like the
database or the files in store/. If this is case, run the following command::

    $ docker-compose up -d --force-recreate --build

Additionally you may want to delete all the data including the stuff in the
external volumes::

    $ make flush

Both snippets can be combined or used separately.


Cleaning up
================================================================================

The most effective way is::

    $ docker-compose down --volumes

The above command will not delete the external volumes described in the
:ref:`installation` section of this document. You must delete the volumes
manually with::

    $ docker volume rm dativebase-old-store

Optionally you may also want to delete the directories on the host::

    $ rm -rf /tmp/dativebase-old-store


.. _`these instructions`: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
.. _`Docker Compose`: https://docs.docker.com/compose/reference/overview/
.. _`docker daemon attack surface`: https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface
.. _`reload`: https://docs.pylonsproject.org/projects/pyramid/en/latest/pscripts/pserve.html#cmdoption-pserve-reload
.. _`Dative`: https://github.com/dativebase/dative
.. _`Online Linguistic Database`: https://github.com/dativebase/old-pyramid
