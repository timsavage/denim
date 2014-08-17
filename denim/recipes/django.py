# -*- coding: utf-8 -*-
from fabric.api import env, put

from denim.constants import DeployUser, RootUser
from denim import paths, webserver, service, django
from denim.recipes.base import ProvisionRecipeBase, DeployRecipeBase


class ProvisionDjangoRecipe(ProvisionRecipeBase):
    """
    A standard provisioning script for django that defaults to using Nginx and Supervisor
    """

    required_packages = ProvisionRecipeBase.required_packages + [
        'nginx',
        'supervisor'
    ]
    required_paths = ProvisionRecipeBase.required_paths + [
        ('{deploy_path}/public/media', DeployUser, 0o755),
        ('{deploy_path}/public/static', RootUser, 0o755),
    ]

    def upload_configuration(self):
        self.step_sub_label("** Web server.")
        webserver.install_config(use_reload=False)

        self.step_sub_label("** Service control.")
        service.install_config()


class DeployDjangoRecipe(DeployRecipeBase):
    """
    Standard deployment recipe for Django applications.
    """
    def deployment(self, revision):
        super(DeployDjangoRecipe, self).deployment(revision)

        self.step_sub_label("Upload environment settings.")
        put(
            paths.local_config_file('app', extension='.py'),
            paths.release_path(sub_path='%s/local_settings.py' % env.package_name),
            use_sudo=True
        )

    def check(self, revision):
        """
        Run any checks that need to be run after the deployment.
        """
        with paths.cd_release(revision):
            django.test_deploy(revision)

    def migrate(self, revision):
        """
        Perform any migration operations that need to be executed.
        """
        self.step_sub_label('Running database migration.')
        with paths.cd_release(revision):
            django.manage('syncdb')
