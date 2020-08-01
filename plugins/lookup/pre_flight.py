from __future__ import absolute_import, division, print_function
import json
from distutils.version import LooseVersion
from pkg_resources import parse_requirements
from six.moves.urllib.request import urlopen

from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_text, to_native
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display


__metaclass__ = type

DOCUMENTATION = r"""
lookup: pre_flight
author:
  - Pulp Team (@pulp) <pulp-dev@redhat.com>
version_added: "2.9"
requirements:
  - disutils
  - json
  - pkg_resources
  - six
short_description: Check if all plugins are compatible with the current pulpcore version.
description:
  - Check if all plugins are compatible with the current pulpcore version.
options:
  terms:
    description: A list of Github termsitories from which to retrieve versions.
    required: True
notes:
  - The version tag is returned however it is defined by the Github termsitory.
  - Most termsitories used the convention 'vX.X.X' for a tag, while some use 'X.X.X'.
  - Some may use release tagging structures other than semver.
  - This plugin does not perform opinionated formatting of the release tag structure.
  - Users should format the value via filters after calling this plugin, if needed.
seealso:
  - name: Github Releases API
    description: API documentation for retrieving the latest version of a release.
    link: https://developer.github.com/v3/terms/releases/#get-the-latest-release
"""

EXAMPLES = r"""
- name: Strip the 'v' out of the tag version, e.g. 'v1.0.0' -> '1.0.0'
  set_fact:
    ansible_version: "{{ lookup('pulp.pulp_installer.pre_flight', 'ansible/ansible')[1:] }}"
- name: Operate on multiple termsitories
  git:
    repo: https://github.com/{{ item }}.git
    version: "{{ lookup('pulp.pulp_installer.pre_flight', item) }}"
    dest: "{{ lookup('env', 'HOME') }}/projects"
  with_items:
    - ansible/ansible
    - ansible/molecule
    - ansible/awx
"""

RETURN = r"""
  _list:
    description:
      - List of latest Github termsitory version(s)
    type: list
"""

display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        pulpcore_version = LooseVersion(to_text(variables["pulp_version"]))
        display.display(
            "pulpcore-{v}".format(v=variables["pulp_version"]),
            color=C.COLOR_WARN
        )
        plugins = variables["pulp_install_plugins"].keys()
        error_messages = []
        for plugin in plugins:
            response = urlopen("https://pypi.org/pypi/{name}/json".format(name=plugin))
            plugin_data = json.load(response)
            plugin_version = plugin_data["info"]["version"]
            display.display(
                "Checking {n}-{v} compatibility".format(n=plugin, v=plugin_version),
                color=C.COLOR_WARN
            )

            for req in plugin_data["info"]["requires_dist"]:
                if "pulpcore" in req:
                    pulpcore_req = next(parse_requirements(to_text(req)))
                    break

            for c, v in pulpcore_req.specs:
                req = LooseVersion(to_text(v))
                result = eval("pulpcore_version{op}req".format(op=c))
                pversion_str = "{plugin}-{version}".format(plugin=plugin, version=plugin_version)

                if not result:
                    err_msg = "{pv} is not compatible with pulpcore-{cv}".format(
                        pv=pversion_str, cv=pulpcore_version
                    )
                    req_msg = "Requirement: {pulpcore_req}".format(pulpcore_req=pulpcore_req)
                    error_message = "{em} - {rq}".format(em=err_msg, rq=req_msg)
                    display.error(to_native(error_message))
                    error_messages.append(to_native(error_message))
                    break

            if pversion_str not in str(error_messages):
                display.display(to_native("{p} - Ok".format(p=pversion_str)), color=C.COLOR_OK)

        if error_messages:
            raise AnsibleError(to_native("\n".join(error_messages)))

        display.vvvv("Success!")
        return to_native("Success!")
