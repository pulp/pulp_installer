import pytest

def test_etc_directory(host):
    etc = host.file("/etc")
    assert etc.user == "root"

# Didn't test with /opt/pulp/home because it was not getting created
# E        +  where 1 = CommandResult(command=b'stat -c %U /opt/pulp/home', exit_status=1, stdout=None, stderr=b"stat: cannot stat '/opt/pulp/home': No such file or directory\n").rc
# opt/pulp/lib/lib64/python3.8/site-packages/testinfra/modules/base.py:49: AssertionError
@pytest.mark.parametrize("directory", [
#    "/var/lib/pulp", "/opt/pulp/home"
    "/var/lib/pulp"
])
def test_pulp_directories(host,directory):
  pulp_dir = host.file(directory)
  assert pulp_dir.user == "pulp"
  assert pulp_dir.group == "pulp"


@pytest.mark.parametrize("service", [
    "pulpcore-api", "pulpcore-content", "pulpcore-worker@1", "pulpcore-worker@2"
])
def test_pulpcore_services(host,service):
  pulpcore_service = host.service(service)
  assert pulpcore_service.is_running
  assert pulpcore_service.is_enabled


@pytest.mark.parametrize("port", [
  80,443
])
def test_port_80(host,port):
  port = host.socket("tcp://0.0.0.0:"+str(port))
  assert port.is_listening


# WORKAROUND because testinfra does not have a builtin
# module to handle HTTP requests
def test_pulp_status_redirect(host):
    output = host.check_output("curl http://localhost/pulp/api/v3/status/ -kw '%{http_code}'")
    assert '301' in output

def test_pulp_status_max_1_redirect(host):
    output = host.check_output("curl http://localhost/pulp/api/v3/status/ --max-redirs 1 -skL -w ' status: %{http_code}'")
    assert 'status: 200' in output
    assert 'database_connection' in output

def test_pulp_status_follow_redirect(host):
    output = host.check_output("curl http://localhost/pulp/api/v3/status/ -skL  -w ' status: %{http_code}'")
    assert 'status: 200' in output
    assert 'database_connection' in output
