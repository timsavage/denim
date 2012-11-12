# -*- encoding:utf8 -*-
try:
    from jinja2 import Environment, PackageLoader
except ImportError:
    raise ImportError('Scaffolding support requires the Jinja 2 templating library to be installed.')

template_environment = Environment(loader=PackageLoader('denim.scaffold'))


def single(template_file, output_name, context):
    """
    Generate a single file.
    :param template_file:
    :param output_name:
    :param context:
    :return:

    """
    template = template_environment.get_template(template_file)
    print template.render(**context)


def environment(template_file, output_name, context):
    """
    Generate multiple files based on the from the env list.
    :param template_file:
    :param output_name:
    :param context:
    :return:

    """
    envs = context.env
    for env in envs:
        context['env'] = env
        single(template_file, output_name, context)


#   Name: (Template, Target, Generation method, Required parameters)
SCAFFOLDS = {
    'nginx': ('nginx.conf.txt', 'conf/nginx/%(env)s.conf', environment, ('env', )),
    'django.fabric': ('django/fabfile.py.txt', 'fabfile.py', single, ('env', ('scm', 'hg'))),
    'django.supervisor': ('django/supervisor.conf.txt', 'conf/supervisor.conf', single, None),
}


def generate_scaffold(scaffold_code):
    scaffold = SCAFFOLDS.get(scaffold_code)
    if not scaffold:
        raise NotImplementedError('This scaffold does not exist')



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

