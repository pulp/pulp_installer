import json
import os
import yaml
from collections import defaultdict
from pathlib import Path

from git import Repo
from redminelib import Redmine
from redminelib.exceptions import ResourceAttrError
from sh import sed


REDMINE_URL = "https://pulp.plan.io"
REDMINE_QUERY_URL = f"{REDMINE_URL}/issues?set_filter=1&status_id=*&issue_id="


def validate_redmine_data(redmine_query_url, redmine_issues):
    """Validate redmine milestone."""
    redmine = Redmine("https://pulp.plan.io")
    project_set = set()
    stats = defaultdict(list)
    milestone_url = "\n[noissue]"
    milestone_id = None
    for issue in redmine_issues:
        redmine_issue = redmine.issue.get(int(issue))

        project_name = redmine_issue.project.name
        project_set.update([project_name])
        stats[f"project_{project_name.lower().replace(' ', '_')}"].append(issue)

        status = redmine_issue.status.name
        if "CLOSE" not in status and status != "MODIFIED":
            stats["status_not_modified"].append(issue)

        try:
            milestone = redmine_issue.fixed_version.name
            milestone_id = redmine_issue.fixed_version.id
            stats[f"milestone_{milestone}"].append(issue)
        except ResourceAttrError:
            stats["without_milestone"].append(issue)

    if milestone_id is not None:
        milestone_url = (
            f"Redmine Milestone: {REDMINE_URL}/versions/{milestone_id}.json\n[noissue]"
        )

    print(f"\n\nRedmine stats: {json.dumps(stats, indent=2)}")
    error_messages = []
    if stats.get("status_not_modified"):
        error_messages.append(
            f"One or more issues are not MODIFIED {stats['status_not_modified']}"
        )
    if stats.get("without_milestone"):
        error_messages.append(
            f"One or more issues are not associated with a milestone {stats['without_milestone']}"
        )
    if len(project_set) > 1:
        error_messages.append(f"Issues with different projects - {project_set}")
    if error_messages:
        error_messages.append(f"Verify at {redmine_query_url}")
        raise RuntimeError("\n".join(error_messages))

    return milestone_url


print("===== Starting the release process =====")
release_path = os.path.dirname(os.path.abspath(__file__))
plugin_path = release_path.split("/.ci")[0]

plugin_name = "pulp_installer"
release_version = input("Please enter the pulp_installer version e.g. (3.12.0): ")
pulpcore_version = input("Please enter the pulpcore version e.g. (3.12.0): ")
pulpcore_selinux_version = input(
    "Please enter the pulpcore-selinux version e.g. (1.2.4): "
)

issues_to_close = []
for filename in Path(f"{plugin_path}/CHANGES").rglob("*"):
    if filename.stem.isdigit():
        issue = filename.stem
        issue_url = f"{REDMINE_URL}/issues/{issue}.json"
        issues_to_close.append(issue)

issues = ",".join(issues_to_close)
redmine_final_query = f"{REDMINE_QUERY_URL}{issues}"
milestone_url = validate_redmine_data(redmine_final_query, issues_to_close)

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
    __pulp_version = yaml.safe_load(f)["__pulp_version"]
    previous_pulpcore_version = __pulp_version.split('"')[1]

with open("roles/pulp_common/defaults/main.yml") as f:
    previous_selinux_version = yaml.safe_load(f)["__pulp_selinux_version"]

with open("galaxy.yml") as f:
    previous_installer_version = yaml.safe_load(f)["version"]

sed(
    [
        "-i",
        f"/^__pulp_version:/s/{previous_pulpcore_version}/{pulpcore_version}/",
        "roles/pulp_common/vars/main.yml",
    ]
)
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
git.commit(
    "-m",
    f"Release {release_version}\n\nRedmine Query: {redmine_final_query}\n{milestone_url}",
)

sha = repo.head.object.hexsha
short_sha = git.rev_parse(sha, short=7)

print(f"\n\nRedmine query of issues to close:\n{redmine_final_query}")
print(f"Release commit == {short_sha}")
print(f"All changes were committed on branch: release_{release_version}")
