#!/usr/bin/env python

# Checks if the pulp plugin has a specific webserver snippet.

# Usage: symlink_snippets.py plugin_name snippet_file

# Usage example: symlink_snippets.py pulp_ansible nginx.conf

# Symlinks the snippet if found.
# Prints to stderr and returns rc 10 if there are snippets, but not the snippet.
# Prints to stderr and rc 1 if plugin is not found.

import os
import importlib
import sys

plugin_name = sys.argv[1]
webserver_conf = sys.argv[2]

plugins = [plugin_name]
if plugin_name == "galaxy_ng":
  plugins.extend(["pulp_ansible", "pulp_container"])

for plugin in plugins:
  try:
    webserver_snippets = importlib.import_module(plugin + ".app.webserver_snippets")
  except ModuleNotFoundError:
    continue
  snippet = os.path.dirname(webserver_snippets.__file__) + "/" + webserver_conf
  if os.path.exists(snippet):
    if "nginx" in webserver_conf:
      try:
        os.symlink(snippet, f"/etc/nginx/pulp/{plugin}.conf")
        print("Symbolic link created successfully")
      except FileExistsError:
        if snippet != os.path.realpath(f"/etc/nginx/pulp/{plugin}.conf"):
          os.unlink(f"/etc/nginx/pulp/{plugin}.conf")
          os.symlink(snippet, f"/etc/nginx/pulp/{plugin}.conf")
      sys.stderr.write(f"{snippet}  and /etc/nginx/pulp/{plugin}.conf")
    elif "apache" in webserver_conf:
      for path in ["/etc/httpd", "/etc/apache2"]:
        if os.path.exists(path):
          try:
            os.symlink(snippet, f"{path}/pulp/{plugin}.conf")
            print("Symbolic link created successfully")
          except FileExistsError:
            if snippet != os.path.realpath(f"{path}/pulp/{plugin}.conf"):
              os.unlink(f"{path}/pulp/{plugin}.conf")
              os.symlink(snippet, f"{path}/pulp/{plugin}.conf")
    else:
      sys.stderr.write(f"Unknown webserver config {webserver_conf}")
      sys.exit(10)
  else:
    sys.stderr.write(plugin + " has snippets, but not " + webserver_conf + "\n")
    sys.exit(10)
