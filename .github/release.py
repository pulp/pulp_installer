import argparse
import os
import textwrap

from git import Repo


REDMINE_QUERY_URL = "https://pulp.plan.io/issues?set_filter=1&status_id=*&issue_id="
release_path = os.path.dirname(os.path.abspath(__file__))
plugin_path = release_path
if ".github" in release_path:
    plugin_path = os.path.dirname(release_path)

with open(f"{plugin_path}/.bumpversion.cfg") as fp:
    release_version = fp.readlines()[1].split("=")[-1].strip()

to_close = []
for filename in os.listdir(f"{plugin_path}/CHANGES"):
    if filename.split(".")[0].isdigit():
        to_close.append(filename.split(".")[0])
issues = ",".join(to_close)

helper = textwrap.dedent(
    """\
        Start the release process.

        Example:
            $ python .github/realease.py

    """
)
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=helper)

parser.add_argument(
    "release_type", type=str, help="Whether the release should be major, minor or patch.",
)

args = parser.parse_args()

release_type = args.release_type

print("\n\nHave you checked the output of: $towncrier --version x.y.z --draft")
print(f"\n\nRepo path: {plugin_path}")
repo = Repo(plugin_path)
git = repo.git

git.checkout("HEAD", b=f"release_{release_version}")

# First commit: changelog
os.system(f"towncrier --yes --version {release_version}")
git.add("CHANGES.rst")
git.add("CHANGES/*")
git.commit("-m", f"Building changelog for {release_version}\n\n[noissue]")

# Second commit: release version
os.system("bump2version release --allow-dirty")

git.add(f"{plugin_path}/galaxy.yml")
git.add(f"{plugin_path}/docs/index.md")
git.add(f"{plugin_path}/roles/pulp/defaults/main.yml")
git.add(f"{plugin_path}/.bumpversion.cfg")
git.commit("-m", f"Releasing {release_version}\n\n[noissue]")

sha = repo.head.object.hexsha
short_sha = git.rev_parse(sha, short=7)

# Third commit: bump to .dev
os.system(f"bump2version {release_type} --allow-dirty")

with open(f"{plugin_path}/.bumpversion.cfg") as fp:
    new_dev_version = fp.readlines()[1].split("=")[-1].strip()


git.add(f"{plugin_path}/galaxy.yml")
git.add(f"{plugin_path}/docs/index.md")
git.add(f"{plugin_path}/roles/pulp/defaults/main.yml")
git.add(f"{plugin_path}/.bumpversion.cfg")
git.commit("-m", f"Bump to {new_dev_version}\n\n[noissue]")

print(f"\n\nRedmine query of issues to close:\n{REDMINE_QUERY_URL}{issues}")
print(f"\nRelease commit == {short_sha}")
