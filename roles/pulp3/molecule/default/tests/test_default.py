import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_sqlite3_db(host):
    f = host.file('/var/lib/pulp/database/pulp.sqlite3')

    assert f.exists
    assert f.user == 'pulp'
    assert f.group == 'pulp'
    assert f.size > 300


def test_services_running(host):
    for sname in ['pulp_web', 'pulp_resource_manager', 'pulp_worker@1',
                  'pulp_worker@2']:
        s = host.service(sname + '.service')
        assert s.is_running
        assert s.is_enabled
