.. image:: https://travis-ci.org/Krast76/onlinectl.svg?branch=master
   :target: https://travis-ci.org/Krast76/onlinectl

onlinectl
=========
Command line tool to interact with online.net

Installation
============

.. code-block:: console

   pip install onlinectl

Authentication
==============

onlinectl < 0.1

.. code-block:: console

   export token='YOUR ONLINE PRIVATE TOKEN'

onlinectl > 0.1

.. code-block:: console

   export ONLINE_TOKEN="YOUR ONLINE PRIVATE TOKEN"

All version support --token option

.. code-block:: console

   onlinectl --token 'YOUR ONLINE PRIVATE TOKEN'

Example
=======

List all servers
~~~~~~~~~~~~~~~~

.. code-block:: console

   $ onlinectl --list
   +--------------+-------+
   |   Hostname   |   id  |
   +--------------+-------+
   |   server1    | 00001 |
   |   server2    | 00002 |
   +--------------+-------+

List available Operating Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

   $ onlinectl --os 00001
   +---------------------+------------------------------+-----+---------+
   |         Name        |           Version            |  id |   arch  |
   +---------------------+------------------------------+-----+---------+
   |        debian       |           Debian 7           | 252 | 64 bits |
   |       windows       |  Windows Datacenter 2012 R2  | 294 | 64 bits |
   |       windows       |   Windows Standard 2012 R2   | 295 | 64 bits |
   |        centos       |          CentOS 6.7          | 296 | 32 bits |
   |        centos       |          CentOS 6.7          | 297 | 64 bits |
   |                            TRUNCATED OUTPUT                        |
   +---------------------+------------------------------+-----+---------+

List all ssh keys
~~~~~~~~~~~~~~~~~

.. code-block:: console

   $ onlinectl --list-keys
   +----------+--------------------------------------+
   |   Nom    |                 UUID                 |
   +----------+--------------------------------------+
   | key1     | 5351d2ae-b3c6-4c61-8ee6-3165b694b077 |
   +----------+--------------------------------------+

Install or reinstall server
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

   $ onlinectl --install --server-id $(SERVER_ID) \
               --os-id $(OS_ID) \
               --hostname $(SERVER_HOSTNAME) \
               --user-login $(USER_LOGIN) \
               --user-password $(USER_PASSWORD) \
               --root-password $(ROOT_PASSWORD) \
               --sshkey-id $(SSH_UUID) \
               --part-template $(TEMPLATE_UUID)

Currently, this command provide no output

TODO
====

* Use only requests instead of slumber

* Use python-cliff instead of argparse and prettytable

* More more functionality
