#!/usr/bin/env python

# Checks if the pulp plugin has a specific webserver snippet.

# Usage: symlink_snippets.py plugin_name snippet_file

# Usage example: symlink_snippets.py pulp_ansible nginx.conf

# If found, prints the filepath.
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
    print(snippet)
  else:
    sys.stderr.write(plugin + " has snippets, but not " + webserver_conf + "\n")
    sys.exit(10)
