import os
import yaml
from pathlib import Path

from git import Repo
from sh import sed


print("===== Starting the release process =====")
release_path = os.path.dirname(os.path.abspath(__file__))
plugin_path = release_path.split("/.ci")[0]

plugin_name = "pulp_installer"
release_version = input("Please enter the pulp_installer version e.g. (3.12.0): ")
pulpcore_version = input("Please enter the pulpcore version e.g. (3.12.0): ")
pulpcore_selinux_version = input(
    "Please enter the pulpcore-selinux version e.g. (1.2.4): "
)

if not release_version:
    raise RuntimeError("pulp_installer version not provided")

if not pulpcore_version:
    raise RuntimeError("pulpcore version not provided")

print("\n\nHave you checked the output of: $towncrier --version x.y.z --draft")
print(f"\n\nRepo path: {plugin_path}")
repo = Repo(plugin_path)
git = repo.git

git.checkout("HEAD", b=f"release_{release_version}")

# First commit: changelog
os.system(f"towncrier --yes --version {release_version}")
git.add("docs/CHANGES.md")
git.add("CHANGES/*")
git.commit("-m", f"Building changelog for {release_version}\n\n[noissue]")


# Second commit: release
with open("roles/pulp_common/vars/main.yml") as f:
    __pulpcore_version = yaml.safe_load(f)["__pulpcore_version"]
    previous_pulpcore_version = __pulpcore_version.split('"')[1]

with open("roles/pulp_common/defaults/main.yml") as f:
    previous_selinux_version = yaml.safe_load(f)["__pulp_selinux_version"]

with open("galaxy.yml") as f:
    previous_installer_version = yaml.safe_load(f)["version"]

sed(
    [
        "-i",
        f"/^__pulpcore_version:/s/{previous_pulpcore_version}/{pulpcore_version}/",
        "roles/pulp_common/vars/main.yml",
    ]
)
if pulpcore_selinux_version:
    sed(
        [
            "-i",
            f"/^__pulp_selinux_version/s/{previous_selinux_version}/{pulpcore_selinux_version}/",
            "roles/pulp_common/defaults/main.yml",
        ]
    )
sed(["-i", f"/^version/s/{previous_installer_version}/{release_version}/", "galaxy.yml"])
prelude = "This version of the installer, "
sed(
    [
        "-i",
        f"0,/{prelude}{previous_installer_version}/s//{prelude}{release_version}/",
        "docs/index.md",
    ]
)
sed(
    [
        "-i",
        f"s/{previous_pulpcore_version}/{pulpcore_version}/",
        "docs/index.md",
    ]
)

git.add("roles/pulp_common/*")
git.add("galaxy.yml")
git.add("docs/index.md")
git.commit("-m", f"Release {release_version}\n\n[noissue]")

sha = repo.head.object.hexsha
short_sha = git.rev_parse(sha, short=7)

print(f"Release commit == {short_sha}")
print(f"All changes were committed on branch: release_{release_version}")
