import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pulp_file_installed(host):
    pkgs = host.pip_package.get_packages(pip_path='/opt/pulp/bin/pip')
    assert 'pulp-file' in pkgs.keys()


def test_pulp_file_migrations_created(host):
    r = host.run('/opt/pulp/bin/python --version')
    assert r.rc == 0

    # Should yield the X.Y version of the used python
    python_version = r.stdout.split(' ')[1][:3]

    fname = '/opt/pulp/lib/python%s/site-packages/pulp_file/app/migrations/' \
        '0001_initial.py' % python_version

    f = host.file(fname)
    assert f.is_file
