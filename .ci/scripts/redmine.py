import os
import sys

from redminelib import Redmine

REDMINE_API_KEY = os.environ["REDMINE_API_KEY"]
REDMINE_QUERY_URL = sys.argv[1]
CLOSED_CURRENTRELEASE = 11

redmine = Redmine(REDMINE_QUERY_URL.split("issues")[0], key=REDMINE_API_KEY)
query_issues = REDMINE_QUERY_URL.split("=")[-1].split(",")

to_update = []
for issue in query_issues:
    status = redmine.issue.get(int(issue)).status.name
    if "CLOSE" not in status and status != "MODIFIED":
        raise ValueError("One or more issues are not MODIFIED")
    if status == "MODIFIED":  # Removing the already closed
        to_update.append(int(issue))

for issue in to_update:
    print(f"Closing #{issue}")
    redmine.issue.update(issue, status_id=CLOSED_CURRENTRELEASE)
