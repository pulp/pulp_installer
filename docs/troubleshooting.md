Troubleshooting
===============


Fixing the "artifacts missing checksum" error
---------------------------------------------

When `allowed_content_checksums` is set:
```yaml
- hosts: all
  vars:
    pulp_settings:
       ...
      allowed_content_checksums:
        - sha1
        - md5
        - sha224
        - sha256
        - sha384
        - sha512
```

The following output can occur:
```
TASK [pulp.pulp_installer.pulp_database_config : Run database migrations] ***********************************************************************************************************************************************
ok: [127.0.0.1]

TASK [pulp.pulp_installer.pulp_database_config : Check if admin account has been created] *******************************************************************************************************************************
fatal: [127.0.0.1]: FAILED! => {"changed": false, "cmd": ["/usr/local/lib/pulp/bin/pulpcore-manager", "shell", "-c", "from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(username=\"admin\").exists())"], "delta": "0:00:03.684104", "end": "2022-05-13 14:13:54.787878", "msg": "non-zero return code", "rc": 1, "start": "2022-05-13 14:13:51.103774", "stderr": "Traceback (most recent call last):  File \"/usr/local/lib/pulp/bin/pulpcore-manager\", line 8, in <module>
    sys.exit(manage())
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/manage.py\", line 11, in manage
    execute_from_command_line(sys.argv)
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/core/management/__init__.py\", line 419, in execute_from_command_line
    utility.execute()
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/core/management/__init__.py\", line 395, in execute
    django.setup()
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/__init__.py\", line 24, in setup
    apps.populate(settings.INSTALLED_APPS)
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/apps/registry.py\", line 114, in populate
    app_config.import_models()
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/apps/config.py\", line 301, in import_models
    self.models_module = import_module(models_module_name)
  File \"/opt/rh/rh-python38/root/usr/lib64/python3.8/importlib/__init__.py\", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File \"<frozen importlib._bootstrap>\", line 1014, in _gcd_import
  File \"<frozen importlib._bootstrap>\", line 991, in _find_and_load
  File \"<frozen importlib._bootstrap>\", line 975, in _find_and_load_unlocked
  File \"<frozen importlib._bootstrap>\", line 671, in _load_unlocked
  File \"<frozen importlib._bootstrap_external>\", line 843, in exec_module
  File \"<frozen importlib._bootstrap>\", line 219, in _call_with_frames_removed
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/models/__init__.py\", line 24, in <module>
    from .exporter import (  # noqa
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/models/exporter.py\", line 11, in <module>
    from pulpcore.app.models.repository import Repository
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/models/repository.py\", line 25, in <module>
    from pulpcore.cache import Cache
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/cache/__init__.py\", line 1, in <module>
    from .cache import Cache, AsyncCache, ContentCache, CacheKeys  # noqa
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/cache/cache.py\", line 7, in <module>
    from pulpcore.app.settings import settings
  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/settings.py\", line 415, in <module>
    raise e
  File \"/usr/local/lib/pulp/lib64/python3
---
.8/site-packages/pulpcore/app/settings.py\"
 line 374, in <module>    raise ImproperlyConfigured(
django.core.exceptions.ImproperlyConfigured: There have been identified artifacts missing checksum 'sha1'. Run 'pulpcore-manager handle-artifact-checksums' first to populate missing artifact checksums."
 "stderr_lines": ["Traceback (most recent call last):"
 "  File \"/usr/local/lib/pulp/bin/pulpcore-manager\" line 8 in <module>"
 "    sys.exit(manage())"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/manage.py\" line 11 in manage"
 "    execute_from_command_line(sys.argv)"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/core/management/__init__.py\" line 419 in execute_from_command_line"
 "    utility.execute()"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/core/management/__init__.py\" line 395 in execute"
 "    django.setup()"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/__init__.py\" line 24 in setup"
 "    apps.populate(settings.INSTALLED_APPS)"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/apps/registry.py\" line 114 in populate"
 "    app_config.import_models()"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/django/apps/config.py\" line 301 in import_models"
 "    self.models_module = import_module(models_module_name)"
 "  File \"/opt/rh/rh-python38/root/usr/lib64/python3.8/importlib/__init__.py\" line 127 in import_module"
 "    return _bootstrap._gcd_import(name[level:] package level)"
 "  File \"<frozen importlib._bootstrap>\" line 1014 in _gcd_import"
 "  File \"<frozen importlib._bootstrap>\" line 991 in _find_and_load"
 "  File \"<frozen importlib._bootstrap>\" line 975 in _find_and_load_unlocked"
 "  File \"<frozen importlib._bootstrap>\" line 671 in _load_unlocked"
 "  File \"<frozen importlib._bootstrap_external>\" line 843 in exec_module"
 "  File \"<frozen importlib._bootstrap>\" line 219 in _call_with_frames_removed"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/models/__init__.py\" line 24 in <module>"
 "    from .exporter import (  # noqa"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/models/exporter.py\" line 11 in <module>"
 "    from pulpcore.app.models.repository import Repository"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/models/repository.py\" line 25 in <module>"
 "    from pulpcore.cache import Cache"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/cache/__init__.py\" line 1 in <module>"
 "    from .cache import Cache AsyncCache ContentCache CacheKeys  # noqa"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/cache/cache.py\" line 7 in <module>"
 "    from pulpcore.app.settings import settings"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/settings.py\" line 415 in <module>"
 "    raise e"
 "  File \"/usr/local/lib/pulp/lib64/python3.8/site-packages/pulpcore/app/settings.py\" line 374 in <module>"
 "    raise ImproperlyConfigured("
 "django.core.exceptions.ImproperlyConfigured: There have been identified artifacts missing checksum 'sha1'. Run 'pulpcore-manager handle-artifact-checksums' first to populate missing artifact checksums."]
 "stdout": ""
 "stdout_lines": []}

NO MORE HOSTS LEFT ******************************************************************************************************************************************************************************************************

PLAY RECAP **************************************************************************************************************************************************************************************************************
127.0.0.1                  : ok=98   changed=1    unreachable=0    failed=1    skipped=58   rescued=0    ignored=0
```

To fix this eror, manually run the `pulpcore-manager` command:
```bash
$ pulpcore-manager handle-artifact-checksums
```

