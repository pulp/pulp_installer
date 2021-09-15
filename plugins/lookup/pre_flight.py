from __future__ import absolute_import, division, print_function
import json
from distutils.version import LooseVersion
from jinja2 import Template
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
"""

EXAMPLES = r"""
- name: Check if plugins are compatible with the current pulpcore version
  set_fact:
    ansible_version: "{{ lookup('pulp.pulp_installer.pre_flight') }}"
"""

RETURN = r"""
  _raw:
    description:
      - Whether or not all plugins are compatible with the current pulpcore version.
    type: str
"""

display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        pulp_version = Template(variables["__pulp_version"]).render()
        pulpcore_version = LooseVersion(to_text(pulp_version))
        display.display(
            "pulpcore-{v}".format(v=pulp_version),
            color=C.COLOR_WARN
        )
        plugins = variables["pulp_install_plugins"].keys()
        error_messages = []
        for plugin in plugins:
            plugin_url = "https://pypi.org/pypi/{name}/json".format(name=plugin)
            _version = variables["pulp_install_plugins"][plugin].get("version")
            if _version:
                plugin_url = "https://pypi.org/pypi/{name}/{version}/json".format(
                  name=plugin, version=_version
                )
            response = urlopen(plugin_url)
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
        return to_native("Compatible!")
