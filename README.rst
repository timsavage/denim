::

      _/_/_/                        _/                        _/          _/_/
     _/    _/    _/_/    _/_/_/        _/_/_/  _/_/        _/  _/      _/    _/
    _/    _/  _/_/_/_/  _/    _/  _/  _/    _/    _/      _/  _/          _/
   _/    _/  _/        _/    _/  _/  _/    _/    _/      _/  _/        _/
  _/_/_/      _/_/_/  _/    _/  _/  _/    _/    _/        _/    _/  _/_/_/_/


A `Fabric <http://www.fabfile.org>`_ deployment strategy for Python web
applications.

Denim has been primarily developed to support Django web applications, deployed
to Debian GNU/Linux (and derivative) platforms. With tools to support nginx,
supervisor, virtual env, gunicorn, pip etc.

Designed to provide a rich tool-set built on top of and working with the
existing functionality provided by Fabric. Get up and running quickly with
the default deployment strategy.

.. image:: https://pypip.in/license/denim/badge.png
    :target: https://pypi.python.org/pypi/denim/
    :alt: License

.. image:: https://pypip.in/v/denim/badge.png
    :target: https://pypi.python.org/pypi/denim/

.. image:: https://travis-ci.org/timsavage/denim.png?branch=master
    :target: https://travis-ci.org/timsavage/denim
    :alt: Travis CI Status

.. image:: https://coveralls.io/repos/timsavage/denim/badge.png?branch=master
    :target: https://coveralls.io/r/timsavage/denim?branch=master
    :alt: Coveralls

.. image:: https://requires.io/github/timsavage/denim/requirements.png?branch=master
    :target: https://requires.io/github/timsavage/denim/requirements/?branch=master
    :alt: Requirements Status

====================
The default strategy
====================

The default strategy describes a project layout and deployment structure for
Django applications that lets you deploy straight away

The strategy is designed to take a freshly deployed server and provision,
deploy and activate your application, using best practices.

By default your application will run as the user *webapps* with a ``/bin/false``
shell and write access to limited parts of the filesystem. All code is owned by
*root*.


Folder Structure
================

Key Variables
-------------

Certain key variables are required to be set in the Fabric ``env`` dictionary,
these should be setup in your *fabfile*:

project_name
  The name of your project, this does not need to be Python compatible (ie you
  can use a dash '-').

package_name
  The name of the python package being deployed, this name is the name of your
  applications package folder (i.e. the django project name).

deploy_env
  The name of the environment you are deploying your application into, this is
  used to determine which configuration should be used. For example production,
  stage, uat.

These key variables will be used throughout this document.


Deployment
----------

+------------------------------------------------+-------------------------------------------+
| /opt/webapps/*project_name*                    | Deploy path                               |
+-+----------------------------------------------+-------------------------------------------+
| | app                                          | Application package deploy path           |
+-+-+--------------------------------------------+-------------------------------------------+
|   | current                                    | The current package version [1]_          |
+---+--------------------------------------------+-------------------------------------------+
|   | *revision*/*package_name*                  | The revision and application package      |
+-+-+--------------------------------------------+-------------------------------------------+
| | bin                                          | Binary folder [2]_                        |
+-+----------------------------------------------+-------------------------------------------+
| | include                                      | Include folder [2]_                       |
+-+----------------------------------------------+-------------------------------------------+
| | lib                                          | Lib folder [2]_                           |
+-+----------------------------------------------+-------------------------------------------+
| | public                                       | Public web root for web server            |
+-+-+--------------------------------------------+-------------------------------------------+
|   | media                                      | Application content or uploaded data [3]_ |
+---+--------------------------------------------+-------------------------------------------+
|   | static                                     | Static application content                |
+-+-+--------------------------------------------+-------------------------------------------+
| | var                                          | Application variable data [3]_            |
+-+-+--------------------------------------------+-------------------------------------------+
|   | wsgi.sock                                  | WSGI socket                               |
+---+--------------------------------------------+-------------------------------------------+
| /var/log/webapps/*project_name*/*package_name* | Project log path [3]_                     |
+------------------------------------------------+-------------------------------------------+

.. [1] Symlink to the current revision.
.. [2] Virtualenv created folders.
.. [3] Writable by application user.

Development
-----------

+--------------------------------+--------------------------------+
| app                            | Application source root        |
+-+------------------------------+--------------------------------+
| | *package_name*               | Application package [5]_       |
+-+-+----------------------------+--------------------------------+
|   | deployment                 | Deployment settings folder     |
+---+-+--------------------------+--------------------------------+
|     | settings.*deploy_env*.py | Environment configuration [4]_ |
+-+---+--------------------------+--------------------------------+
| | requirements.txt             | PIP requirements file          |
+-+------------------------------+--------------------------------+
| conf                           | Configuration                  |
+-+------------------------------+--------------------------------+
| | init.d                       | Startup scripts for init.d     |
+-+------------------------------+--------------------------------+
| | nginx                        | Nginx configuration            |
+-+-+----------------------------+--------------------------------+
|   | nginx.*deploy_env*.conf    | Environment configuration [4]_ |
+---+----------------------------+--------------------------------+
| fabfile.py                     | Project fabric definition file |
+-+------------------------------+--------------------------------+

.. [4] Used to apply specific configuration based on deployment environment.
.. [5] This structure is based on Django 1.4.
