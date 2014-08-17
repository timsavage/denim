# -*- coding: utf-8 -*-
from fabric import colors
from fabric.api import sudo, abort
from fabric.context_managers import cd
from fabric.contrib.files import exists
from fabric.operations import require
from fabric.state import env
from fabric.tasks import Task

from denim import (package, paths, pip, service, system)
from denim.constants import RootUser, DeployUser
from denim.decorators import cached_property
from denim.utils import run_as, run_test


class RecipeBase(Task):
    """
    Base class for recipes.
    """
    # Additional path appended to the deploy path.
    deploy_path_suffix = ''
    # Additional path append to log path.
    log_path_suffix = ''

    def __init__(self, params=None, *args, **kwargs):
        super(RecipeBase, self).__init__(*args, **kwargs)
        if params:
            self.__dict__.update(params)

    def run(self):
        raise NotImplementedError()

    @cached_property
    def deploy_root(self):
        return paths.project_path(self.deploy_path_suffix)

    @cached_property
    def log_root(self):
        return paths.log_path(self.log_path_suffix)

    @staticmethod
    def step_label(label):
        print(colors.yellow("* %s" % label))

    @staticmethod
    def step_sub_label(label):
        print(colors.cyan("** %s" % label))


def check_optional_item(item):
    if isinstance(item, (list, tuple)):
        item, check = item
        if callable(check):
            check = check()
        if check:
            return item
    else:
        return item


class ProvisionRecipeBase(RecipeBase):
    """
    Base class for provisioning recipes.
    """
    # Base packages required.
    required_packages = ['python', 'git', 'python-pip']
    # Install packages that are missing
    install_missing_packages = True
    # Default paths
    required_paths = [
        ('{deploy_path}', RootUser, 0o755),
        ('{deploy_path}/releases', RootUser, 0o755),
        ('{deploy_path}/public', RootUser, 0o755),
        ('{deploy_path}/var', DeployUser, 0o755),
        ('{log_path}', DeployUser, 0o755),
    ]

    def run(self):
        require('project_name', 'package_name', 'deploy_env')

        self.step_label('Check correct packages are installed.')
        self.ensure_packages()

        self.step_label('Check application run user exists.')
        self.ensure_user()

        self.step_label('Create deployment paths and set permissions.')
        self.create_paths()

        self.step_label("Upload configuration for dependant services.")
        self.upload_configuration()

    def ensure_packages(self):
        """
        Ensure that the correct packages have been installed.
        """
        packages = (check_optional_item(p) for p in self.required_packages)
        if self.install_missing_packages:
            run_as("apt-get update", use_sudo=True, user=RootUser)
            package.ensure_installed(*packages)
        else:
            missing_packages = package.check_installed(*packages)
            if missing_packages:
                abort('The following package(s) are not installed: %s' % ', '.join(missing_packages))

    def ensure_user(self):
        """
        Ensure the system user has been created.
        """
        system.create_system_user()

    def create_paths(self):
        """
        Create deployment paths.
        """
        for path, user, mode in self.required_paths:
            path = path.format(
                deploy_path=self.deploy_root,
                log_path=paths.log_path()
            )
            sudo('mkdir -p %s' % path)
            system.change_owner(path, user=user)
            system.change_mode(path, mode)

    def upload_configuration(self):
        """
        Upload any specific configuration that is required for the server or other services.
        """
        pass


class DeployRecipeBase(RecipeBase):
    """
    Base class for deployment recipes.
    """
    deploy_cache_root = '~/.deploy-cache/'

    def run(self, revision):
        require('project_name', 'package_name', 'deploy_env', 'scm_repository')

        env.revision = revision

        self.step_label('Pre deployment steps.')
        self.pre_deployment(revision)

        self.step_label('Deployment steps.')
        self.deployment(revision)

        self.step_label('Applying library updates.')
        self.update(revision)

        self.step_label('Running post deployment checks.')
        self.check(revision)

        self.step_label('Migrate any data.')
        self.migrate(revision)

        self.step_label('Make this revision the current one.')
        self.make_current(revision)

        self.step_label('Restart the application.')
        self.restart(revision)

    def get_deploy_cache_path(self, repository_name=None):
        if repository_name is None:
            repository_name = env.project_name
        return paths.join_paths(self.deploy_cache_root, repository_name)

    @cached_property
    def deploy_cache_path(self):
        """
        Path to the current deployment repository cache (the git root).
        """
        return self.get_deploy_cache_path()

    def populate_git_cache(self, repository_name, repository_uri, revision):
        """
        Populate the local git cache
        """
        if not exists(self.deploy_cache_root):
            run_as('mkdir -p %s' % self.deploy_cache_root)

        git_cache_path = self.get_deploy_cache_path(repository_name)

        if not exists(git_cache_path):
            run_as('git clone %s %s' % (repository_uri, git_cache_path))

        with cd(git_cache_path):
            run_as('git pull')

            self.step_sub_label('Check requested revision is in place.')
            result = run_as('git tag | grep %s | wc -l' % revision)
            if result != '1':
                abort('Could not find revision `%s` in deploy cache for %s.' % (revision, repository_name))

    def pre_deployment(self, revision):
        """
        Any tasks that need to be completed prior to deployment.

        ie update git cache, building deployment bundle, collect static files etc. Update S3...
        """
        self.step_sub_label('Update deploy cache')
        self.populate_git_cache(env.project_name, env.scm_repository, revision)

    def deployment(self, revision):
        """
        Actual deployment of the application.

        ie copy code into release folder, upload deployment bundle and unzip.
        """
        self.step_sub_label('Deploy revision into releases folder.')
        if not exists(paths.release_path(revision)):
            local_src_root = env.get('local_src_root', 'src')
            with cd(self.deploy_cache_path):
                run_as('git archive --format=tar %s %s | tar -x -C %s' % (
                    revision, local_src_root, paths.deploy_path('releases')), use_sudo=True)
            with paths.cd_deploy('releases'):
                run_as('mv %s %s' % (local_src_root, revision), use_sudo=True)

    def update(self, revision):
        """
        Update any libraries.

        ie update requirements.
        """
        self.step_sub_label('Update requirements.')
        pip.install_requirements(revision)

    def check(self, revision):
        """
        Run any checks that need to be run after the deployment.
        """

    def migrate(self, revision):
        """
        Perform any migration operations that need to be executed.
        """

    def make_current(self, revision):
        """
        Swap current release symlink to this release.
        """
        self.step_sub_label("Symlinking to current")

        current_symlink = paths.deploy_path('current')

        run_test('rm -f ' + current_symlink, use_sudo=True)
        system.create_symlink(
            paths.release_path(revision),
            current_symlink,
            use_sudo=True, user=RootUser
        )

    def restart(self, revision):
        """
        Restart the application to make the new deployment active.
        """
        print colors.cyan("** Restart service")
        service.restart()