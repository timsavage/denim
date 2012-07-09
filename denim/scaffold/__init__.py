# -*- encoding:utf8 -*-
try:
    from jinja2 import Environment, PackageLoader
except ImportError:
    raise ImportError('Scaffolding support requires the Jinja 2 templating library to be installed.')

template_environment = Environment(loader=PackageLoader('denim.scaffold'))

#template = template_environment.get_template('django/fabfile.py.txt')
#context = {
#    'deploy_scm': 'git',
#    'deployment_envs': [{
#        'name': 'production',
#        'hosts': ['192.168.0.1', '192.168.0.2',]
#    }, {
#        'name': 'staging',
#        'hosts': ['192.168.1.1', '192.168.1.2',]
#    }, {
#        'name': 'development',
#        'hosts': ['127.0.0.1',]
#    }]
#}
#print template.render(**context)
