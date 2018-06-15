pulp3-workers
=============

Install, configure, and set the state of pulp workers.

This role accepts one optional variable, `pulp3_workers`. It's a dict with the
following structure:

```yaml
1:
  state: started
  enabled: true
2:
  state: started
  enabled: true
```

If the variable is set to this value, two workers will be created, both started
and enabled.
