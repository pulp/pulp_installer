Release Guide
=============

1. Ensure that pulpcore of the corresponding version is available on PyPI.
1. Generate changelog (`towncrier --yes --version 3.8.0`).
1. Update version in the `galaxy.yml` and in the `roles/pulp_common/defaults/main.yml`.
1. Update references to current and previous versions in `docs/index.md`
   (`sed -i -e 's/3.7.1/3.8.0/g' -e 's/3.6.z/3.7.z/g' -e 's/3.5.z/3.6.z/g' docs/index.md`).\
   **NOTE**: Post releases are done in pulp_installer as needed.
   The format is in compliance with [PEP 440 for implicit post releases](https://www.python.org/dev/peps/pep-0440/#implicit-post-releases), e.g. 3.7.0-1.
1. Create a PR with all the changes above and merge it after a review.
1. Tag this commit with the name of the release, e.g. 3.8.0.
1. Create a release on github based on the tag.
1. Upload the pulp_installer collection to the Galaxy.


Uploading a collection to the Galaxy
------------------------------------

1. Prepare a tarball of the pulp_insaller collection (from inside the root of the collection, run `ansible-galaxy collection build`).\
   **NOTE**: ansible-galaxy>=2.9 is reqiured.
1. Make sure that you are one of the owners on Galaxy! Github perms are not helping here.
1. Go to https://galaxy.ansible.com/my-content/namespaces.
1. Choose/unfold pulp namespace.
1. "Upload new verison" to the pulp_installer collection.
