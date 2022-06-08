import pytest

def test_etc_directory(host):
    etc = host.file("/etc")
    assert etc.user == "root"


def test_pulp_home(host):

  pulp_home = host.file("/opt/pulp/home")
  pulp_dir = host.file("/var/lib/pulp")

  if pulp_home.exists:
    assert pulp_home.user == "pulp"
    assert pulp_home.group == "pulp"
  elif pulp_dir.exists:
    assert pulp_dir.user == "pulp"
    assert pulp_dir.group == "pulp"
  else:
    assert False


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
    output = host.check_output("curl http://localhost/pulp/api/v3/status/ -o/dev/null -skw '%{http_code}'")
    assert '301' in output


def test_pulp_status_max_1_redirect(host):
    output = host.check_output("curl http://localhost/pulp/api/v3/status/ --max-redirs 1 -skL -w ' status: %{http_code}'")
    assert 'status: 200' in output
    assert 'database_connection' in output

def test_pulp_status_follow_redirect(host):
    output = host.check_output("curl http://localhost/pulp/api/v3/status/ -skL  -w ' status: %{http_code}'")
    assert 'status: 200' in output
    assert 'database_connection' in output

