.. include:: ../../README.rst

Environment Variables
=====================

Photon will use a copy of the existing environment to pass to its call to
``ansible-playbook``. This allows you to preserve your venv when using photon.
You can add to or overwrite environment variables in the ``azs.<name>.env``
section of your config.

.. code-block:: yaml

    azs:
      proxmox:
        inventory: path/to/inventory
        # added to existing environment
        env:
          ANSIBLE_VAULT_PASSWORD_FILE: path/to/vault.pass

Workflow Flags
==============

Flags are simply CLI options that are passed to the underlying call to
``ansible-playbook``. When defined as ``workflows.<name>.flags`` they will be
applied to all playbooks in a workflow. When defined as
``workflows.<name>.playbooks.<playbook>.flags`` they will be applied only to
that specific playbook.

.. code-block:: yaml

    workflows:
      test_password_playbooks:
        flags:
          # applied to all playbooks in this workflow
          - --become
          - --connection=ssh
        playbooks:
          - path: playbooks/tests/update_passwords.yml
            # applied to only this playbook
            flags:
              - --tags=tag1,tag2
              - --extra-vars=mysql_in_use=True

Limiting Execution
==================

By default, all workflows can be executed against all AZs. It is possible
to limit a workflow to only run against limited AZs. For example, a
workflow that tests password change playbooks makes sense against proxmox,
but would be destructive if run against a production AZ.

A workflow can be limited by adding the key ``workflows.<name>.allowed_azs``.

.. code-block:: yaml

    azs:
      proxmox:
        inventory: path/to/proxmox/inventory
      production:
        inventory: path/to/production/inventory
    workflows:
      test_password_playbooks:
        # will error if workflow is run against the az production
        allowed_azs:
          - proxmox
        playbooks:
          - path: playbooks/tests/test_passwords.yml

Resuming Execution
==================

In the event of a playbook failure, photon will print a command as part of the
error message that can be used to continue the execution of a workflow from the
point where it failed. This is simply a list index that corresponds to the
position of a playbook in ``workflows.<workflow>.playbooks``.

.. code-block:: yaml

    workflows:
      test_password_playbooks:
        playbooks:
          - path: playbooks/tests/mysql_password.yml
          - path: playbooks/tests/rabbitmq_password.yml
          - path: playbooks/tests/some_other_password.yml
          - path: playbooks/tests/another_password.yml

Using the above config, the command:

.. code-block:: bash

    $ photon test_password_playbooks proxmox --resume 3

Would resume execution starting with the ``some_other_password.yml`` playbook.

.. toctree::
   :maxdepth: 3

   testing
   contributing
   development
   changelog
   authors

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
