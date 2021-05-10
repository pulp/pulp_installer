Release Guide
=============

1. Ensure that pulpcore of the corresponding version is available on PyPI.
1. Run the release script (`python .ci/scripts/release.py`).
1. Check the updated version in the `galaxy.yml` and in the `roles/pulp_common/{vars,defaults}/main.yml`.
1. Check references to current and previous versions in `docs/index.md`\
   **NOTE**: Post releases are done in pulp_installer as needed.
   The format is in compliance with [PEP 440 for implicit post releases](https://www.python.org/dev/peps/pep-0440/#implicit-post-releases), e.g. 3.7.0-1.
1. Create a PR with all the changes above and merge it after a review.
1. Tag this commit with the name of the release, e.g. 3.8.0.
1. Create a release on github based on the tag.


## Manually uploading a collection to the Galaxy

For older releases of pulp_installer, you may have to manually upload the collection to galaxy.ansible.com.

1. Prepare a tarball of the pulp_insaller collection (from inside the root of the collection, run `ansible-galaxy collection build`).\
   **NOTE**: ansible-galaxy>=2.9 is required.\
   **NOTE:** the tarball will include every untracked file in the repo unless you git clean, even
ignored files. You may want to just clone the repo to another temporary dir instead.
1. Make sure that you are one of the owners on Galaxy! Github perms are not helping here.
1. Go to https://galaxy.ansible.com/my-content/namespaces.
1. Choose/unfold pulp namespace.
1. "Upload new verison" to the pulp_installer collection.
