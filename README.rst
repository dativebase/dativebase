================================================================================
  DativeBase = `Dative`_ + the `Online Linguistic Database`_
================================================================================

DativeBase is the entrypoint for Dative/OLD: software for collaborative
language documentation and analysis.

This repository is the hub for deployment strategies for Dative and the OLD. It
contains two `Docker Compose`_ configurations for local deployments.

1. `HTTP Deploy`_ (recommended)
2. `HTTPS Deploy`_ (error-prone but more like production)

.. _`Dative`: https://github.com/dativebase/dative
.. _`Online Linguistic Database`: https://github.com/dativebase/old-pyramid
.. _`HTTP Deploy`: docker-compose-http/README.rst
.. _`HTTPS Deploy`: docker-compose/README.rst
.. _`Docker Compose`: https://docs.docker.com/compose/overview/
