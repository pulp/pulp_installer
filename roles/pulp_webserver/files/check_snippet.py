#!/usr/bin/env python

# Checks if the pulp plugin has a specific webserver snippet.

# Usage: check_snippet.py plugin_name snippet_file

# Usage example: check_snippet.py pulp_ansible nginx.conf

# Prints full path to the snippet to stdout and returns rc 0 if found.
# Prints to stderr and returns rc 10 if there are snippets, but not the snippet.
# Prints to stderr and rc 1 if plugin is not found.

import os
import importlib
import sys
webserver_snippets = importlib.import_module(sys.argv[1] + ".app.webserver_snippets")
snippet = os.path.dirname(webserver_snippets.__file__) + "/" + sys.argv[2]
if os.path.exists(snippet):
  print(snippet)
else:
  sys.stderr.write(sys.argv[1] + " has snippets, but not " + sys.argv[2] + "\n")
  sys.exit(10)
