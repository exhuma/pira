import fabric.api as fab

fab.env.roledefs = {
    'prod': ['192.168.1.20']
}
fab.env.user = 'pi'


@fab.task
def deploy():
    fab.local('python setup.py sdist')
    name = fab.local('python setup.py --fullname', capture=True).strip()
    filename = name + '.tar.gz'
    fab.put('dist/' + filename, '/tmp')
    with fab.cd('/opt'):
        fab.run('./pira/bin/pip install /tmp/{}.tar.gz'.format(name))
    fab.run('rm /tmp/' + filename)
