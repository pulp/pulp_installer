# Chris Meyers

from ansiblelint import AnsibleLintRule


class FileTypeModuleHasMode(AnsibleLintRule):
    """ test it """

    id = 'ANSIBLE921'
    shortdesc = "Ensure mode is explicitly set"
    description = "Ensure mode is explicitly set when a new file COULD potentially be created"
    tags = ['mode', 'file']

    _commands = ['acl', 'archive', 'assemble', 'copy', 'fetch', 'file', 'ini_file', 'iso_extract', 'lineinfile', 'patch', 'tempfile', 'template', 'unarchive', 'xattr']

    def matchtask(self, file, task):
        if task["action"]["__ansible_module__"] in self._commands:
            if task["action"].get("state", "present") == "absent":
                return False
            return not bool(task["action"].get('mode', False))
        return False
