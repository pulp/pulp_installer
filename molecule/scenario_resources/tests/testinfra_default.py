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

def test_certs_dir(host):

  certs_dir = host.file("/etc/pulp/certs")
  certs_dir_alt = host.file("/opt/pulp/etc/certs")

  if certs_dir.exists:
    assert certs_dir.user == "pulp"
    assert certs_dir.group == "pulp"
  elif certs_dir_alt.exists:
    assert certs_dir_alt.user == "pulp"
    assert certs_dir_alt.group == "pulp"
  else:
    assert False

def test_pulp_static_dir(host):

  galaxy_installed_dir = host.file("/etc/galaxy-importer")
  static_dir = host.file("/var/lib/pulp/assets")
  static_dir_alt = host.file("/opt/pulp/assets")
  static_dir_galaxy = host.file("/var/lib/pulp/static")

  if galaxy_installed_dir.exists:
    assert static_dir_galaxy.user == "pulp"
    assert static_dir_galaxy.group == "pulp"
  elif static_dir.exists:
    assert static_dir.user == "pulp"
    assert static_dir.group == "pulp"
  elif static_dir_alt.exists:
    assert static_dir_alt.user == "pulp"
    assert static_dir_alt.group == "pulp"
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


def test_pulp_status_max_2_redirect(host):
    output = host.check_output("curl http://localhost/pulp/api/v3/status/ --max-redirs 2 -skL -w ' status: %{http_code}'")
    assert 'status: 200' in output
    assert 'database_connection' in output

def test_pulp_status_follow_redirect(host):
    output = host.check_output("curl http://localhost/pulp/api/v3/status/ -skL  -w ' status: %{http_code}'")
    assert 'status: 200' in output
    assert 'database_connection' in output

