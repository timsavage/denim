# -*- encoding:utf8 -*-
"""
Common deployment recipes.

Provision
=========

- Create system user
- Create folder layout
- Create virtual env
- Deploy web-server configuration
- Test web-server configuration
- Reload web-server configuration
- Initial deployment
- Deploy init scripts

Deployment
==========

- Archive SCM release
- Upload and extract archive
- Install requirements

Django specific items
- Symlink Django environment specific settings
- Run collect static to migrate over content (also tests settings are correct)
- Display migrations that need to be run (south), warning only if south isn't present.

- Symlink new release as current

"""
from fabric import colors
from fabric.api import abort, env, prompt, put, require, sudo
from fabric.contrib import files
from denim import (package, paths, pip, service, scm, system, utils,
                   virtualenv, webserver)


# These are the default packages for Nginx, PostgreSQL and Supervisor for
# Debian GNU/Linux or derivatives.
DEFAULT_PACKAGES = [
    'nginx', # Web server
    'supervisor', # Process Manager

    # Python requirements
    'python',
    'python-crypto',
    'python-virtualenv',
    ]


class RecipeMetaclass(type):
    def __new__(cls, name, bases, attrs):
        print 'cls:', cls
        print 'name', name
        print 'bases', bases
        print 'attrs', attrs
        return type.__new__(cls, name, bases, attrs)



class Recipe(object):
    """
    Recipe definition.
    """
    __metaclass__ = RecipeMetaclass

    def bake(self, *args, **kwargs):
        """
        Bake this recipe!
        """
        # Get the steps involved
        print self.__dict__
        step_names = [n for n in self.__dict__.iterkeys() if n.startswith('step_')]
        for name in step_names:
            step = self.__dict__[name]

            # Determine label
            if step.__doc__:
                operation, _, _ = step.__doc__.partition('\n')
            else:
                operation = name[6:].replace('_', ' ').strip().capitalize()
            print colors.yellow("* " + operation)

#            step()

    def __call__(self, *args, **kwargs):
        self.bake(*args, **kwargs)


class StandardProvisionRecipe(Recipe):
    def __init__(self, packages=DEFAULT_PACKAGES):
        self.packages = packages

    def bake(self, extra_packages=None, handle_os_changes=True):
        require('project_name', 'package_name', 'deploy_env', 'deploy_user')

        if extra_packages:
            self.packages.append(extra_packages)
        self.handle_os_changes = handle_os_changes

        self.deploy_path = paths.deploy_path()
        self.log_path = paths.log_path()

        super(StandardProvisionRecipe, self).bake()

    def step_install_packages(self):
        """
        Check correct packages are installed.

        Will install packages if needed. This behaviour can be prevented by
        initializing
        """
        for package_name in self.packages:
            if not package.is_installed(package_name):
                if self.handle_os_changes:
                    package.install(package_name)
                else:
                    abort('Package "%s" is not available on the server.' % package_name)

    def step_ensure_user_exists(self):
        """
        Ensure user this application will run as exists.
        """
        if not system.user_exists(env.deploy):
            if self.handle_os_changes:
                system.create_system_user()
            else:
                abort('Application user "%s" does not exist on deployment server.' % env.deploy_user)

    def step_create_standard_layout(self):
        """
        Create standard deployment layout.
        """
        deploy_path = self.deploy_path
        log_path = self.log_path

        # Create paths
        sudo('mkdir -p %s/{app,public,var}' % deploy_path)
        sudo('mkdir -p %s/public/{media,static}' % deploy_path)
        sudo('mkdir -p %s' % log_path)

        # Set correct user for application writable paths.
        system.change_owner(paths.join_paths(deploy_path, 'var'))
        system.change_owner(paths.join_paths(deploy_path, 'public/media'))
        system.change_owner(log_path)

    def step_create_virtualenv(self):
        """
        Create virtual env
        """
        virtualenv.create()

standard_provision = StandardProvisionRecipe()


def archive_and_upload(revision, noinput=False, use_sudo=True, user=None):
    """
    Upload application archive based on a source control revision.

    :param revision: revision to deploy.
    :return: name of the revision that was deployed.

    """
    # Archive and upload package
    archive_file, revision_name = scm.archive_app(revision)
    put(archive_file, '/tmp/%s' % archive_file)

    with paths.cd_deploy('app'):
        # Extract package
        utils.run_as('tar -xf /tmp/%s' % archive_file, use_sudo, user)

        # Correct path name
        if files.exists(revision_name):
            if noinput or utils.confirm(colors.red('A revision with the same name already exists, overwrite?')):
                utils.run_as('rm -rf %s' % revision_name, use_sudo, user)
        utils.run_as('mv app %s' % revision_name, use_sudo, user)
    return revision_name


def create_standard_layout():
    """
    Create standard deployment layout.
    """
    deploy_path = paths.deploy_path()
    log_path = paths.log_path()

    # Create paths
    sudo('mkdir -p %s/{app,public,var}' % deploy_path)
    sudo('mkdir -p %s/public/{media,static}' % deploy_path)
    sudo('mkdir -p %s' % log_path)

    # Set correct user for application writable paths.
    system.change_owner(paths.join_paths(deploy_path, 'var'))
    system.change_owner(paths.join_paths(deploy_path, 'public/media'))
    system.change_owner(log_path)


def old_standard_provision(required_packages=DEFAULT_PACKAGES,
                       install_packages=True):
    """
    Standard provisioning recipe.

    :param required_packages: list of packages that are required on the server.
    :param install_packages: indicates if packages should be installed if they
        are not on the server.

    If `install_packages` is `False` and a package is missing provisioning will
    abort.
    """
    require('project_name', 'package_name', 'deploy_env')

    print colors.yellow("* Check correct packages are installed.")
    for package_name in required_packages:
        if not package.is_installed(package_name):
            if install_packages:
                package.install(package_name)
            else:
                abort('* Package "%s" is not available on the server.' % package_name)

    print colors.yellow("* Create standard layout.")
    system.create_system_user()
    create_standard_layout()
    virtualenv.create()

    print colors.yellow("* Upload configuration for dependant services.")
    print colors.cyan("** Web server.")
    webserver.install_config()
    print colors.cyan("** Service control.")
    service.install_config()


def standard_deploy(revision, noinput=False, use_pip_bundle=False):
    """
    Standard deployment recipe.

    :param revision: revision of the app to work on.
    :param use_pip_bundle: Create a pip bundle to install packages.

    """
    require('project_name', 'package_name', 'deploy_env')

    print colors.yellow("* Archive and upload requested revision.")
    env.revision = archive_and_upload(revision, noinput)

    with virtualenv.activate():
        print colors.yellow("* Install requirements.")
        if use_pip_bundle:
            bundle_file = pip.create_bundle_from_revision(env.revision)
            pip.install_bundle(bundle_file)
        else:
            pip.install_requirements(revision=env.revision, use_sudo=True)

    return env.revision


def standard_django_deploy(revision=None, noinput=False,
                           enable_south_migrations=True):
    """
    Standard django deployment

    :param revision: revision of the app to work on.
    :param noinput: do not ask for any input just automatically migrate.
    :param revision: Do checks with south.

    .. note::
        This section follows on after the ``standard_deploy``.

    """
    import django
    from django import south

    if not revision:
        revision = env.revision

    with virtualenv.activate():
        print colors.yellow("* Setup Django deployment.")

        print colors.cyan("** Symlink in environment settings.")
        django.link_settings(revision)

        print colors.cyan("** Collect static assets.")
        django.collectstatic(revision)

        if enable_south_migrations:
            print colors.cyan("** Display unapplied revisions")
            south.show_migrations(revision, True)
            msg = "Sync models and apply migrations?"
        else:
            msg = "Sync models?"

        if noinput or utils.confirm(msg):
            print colors.cyan("** Syncing models")
            django.syncdb(revision)

            if enable_south_migrations:
                print colors.cyan("** Applying migrations")
                south.migrate(revision)
