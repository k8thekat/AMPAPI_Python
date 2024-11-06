from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# Grab Version from __init__.py
version = ""
_cwd = Path().cwd().joinpath("../../../").resolve()
with _cwd.joinpath("ampapi/__init__.py").open() as file:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type:ignore

if not version:
    raise RuntimeError("version is not set")

# Grab Version from `CHANGELOG.md`
with _cwd.joinpath("./CHANGELOG.md").open() as changelog:
    changelog_data = changelog.read()
    split_data = changelog_data.split("\n")
    ver_data = split_data[0]  # Version - *.*.*** (commit hash)
    ver_data = ver_data.split(" ")
    last_commit: str = ver_data[-1][1:8]
    cl_ver: str = ver_data[-3]
    changelog.close()

# Compare CHANGELOG.md and __init__.py Versions.
if version == cl_ver:
    raise ValueError(f"Version has not been updated `__init__.py`: {version} == `CHANGELOG.md`: {cl_ver}")

# Verify that the current branch is `developer`.
output: bytes = subprocess.check_output(["git", "branch"])
branch: str = output.decode("utf-8").strip("*").strip().split("\n")[0]
if branch != "developer":
    raise RuntimeError(f"Current branch is not `developer`: {branch}")

# Verify that there are new commits.
output = subprocess.check_output(["git", "log"])
new_commit = output.decode("utf-8").split("\n")[0][7:14]
if new_commit == last_commit:
    raise RuntimeError(f"No new commits since last version: {last_commit} == {new_commit}")

# Format the git log data into a dictionary for Changelog.
output = subprocess.check_output(["git", "log", '--format="%B"', last_commit + "..HEAD"])
files: dict[str, list[str]] = {}
cur_data = output.decode("utf-8")
cur_data = cur_data.strip().strip('"')
cur_data = cur_data.split("\n")
file_name = None
for entry in cur_data:
    if len(entry) == 0 or len(entry) == 1:
        continue
    if entry.startswith("$"):
        # This should skip our auto generated changelog commit from Github Actions.
        continue

    if entry.startswith('"'):
        entry = entry.strip('"')

    elif entry.startswith("#"):
        file_name = entry[1:].strip()
        if file_name not in files:
            files[file_name] = []

    else:
        if entry.startswith("--"):
            entry = "\t-" + entry[2:]
        if file_name is None:
            file_name = "Overall"
            files[file_name] = []
        files[file_name].append(entry)


# Format the data into the `CHANGELOG.md`
user = "k8thekat"
project = "AMPAPI_Python"
set_version = f"## Version - {version} - [{new_commit[:7]}](https://github.com/{user}/{project}/commit/{new_commit})\n"
add_changelog: str = f"#### Changelog.md\n- Version info from `{cl_ver}` added.\n"
add_init: str = f"#### __init__.py\n- Version bump to `{version}`\n\n"
data = set_version + add_changelog + add_init
for file_name, file_changes in files.items():
    data: str = data + "#### " + file_name + "\n" + "\n".join(file_changes) + "\n\n"

data = data + changelog_data
with _cwd.joinpath(
    "./CHANGELOG.md",
).open("w") as changelog:
    changelog.write(data)
    changelog.close()

# Github Actions Checkout/Commit
# id | k8thekat = 68672235
subprocess.run(["git", "config", "user.name", "github-actions[bot]"])
subprocess.run(["git", "config", "user.email", "68672235+github-actions[bot]@users.noreply.github.com"])
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f"$ Autogenerated Changelog for {version}"])
subprocess.run(["git", "push", "--force"])
