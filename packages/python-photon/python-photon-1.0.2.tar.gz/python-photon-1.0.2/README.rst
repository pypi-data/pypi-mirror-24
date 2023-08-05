******
Photon
******

.. image:: https://badge.fury.io/py/python-photon.svg
   :target: https://badge.fury.io/py/python-photon
   :alt: PyPI Package

.. image:: https://readthedocs.org/projects/python-photon/badge/?version=latest
   :target: https://python-photon.readthedocs.io/en/latest/
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-MIT-brightgreen.svg
   :target: LICENSE
   :alt: Repository License

Photon is a data driven tool designed to run workflows against an AZ using
Ansible.

A workflow is comprised of one more more playbooks, each configurable
with its own flags and options to be passed down to underlying call to
``ansible-playbook``. It supports the ability to resume a workflow from any
point in the event of a playbook failure.

Quick Start
===========

Install photon using pip:

.. code-block:: bash

    $ pip install python-photon

Create a file called ``photon.yml`` and define at least one AZ and workflow.

.. code-block:: yaml

    azs:
      proxmox:
        inventory: path/to/inventory
    workflows:
      test_password_playbooks:
        playbooks:
          - path: playbooks/tests/update_passwords.yml

.. important::
    ``azs.<name>.inventory`` is the only required value when defining an AZ.
    ``workflows.<name>.playbooks`` is the only required value when defining a
    workflow.

To execute a workflow against an AZ, simply run:

.. code-block:: bash

    $ photon test_password_playbooks proxmox

Documentation
=============

https://python-photon.readthedocs.io/

License
=======

`MIT`_

.. _`MIT`: https://github.com/metacloud/photon/blob/master/LICENSE

The logo is licensed under the `Creative Commons NoDerivatives 4.0 License`_.
If you have some other use in mind, contact us.

.. _`Creative Commons NoDerivatives 4.0 License`: https://creativecommons.org/licenses/by-nd/4.0/
