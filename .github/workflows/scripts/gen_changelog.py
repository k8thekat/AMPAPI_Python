# ruff: noqa
import pathlib
import subprocess  # noqa: S404
from pathlib import Path
import re
import sys

# Unique information for the project.
user = "k8thekat"
gitHub_repo_name: str = "AMPAPI_Python"
project_name: str = "ampapi"
project_dir: pathlib.Path = pathlib.Path().joinpath(project_name)
project_branch: str = "developer"
repo_url = f"https://github.com/k8thekat/{gitHub_repo_name}"

# New Repo Initialization only.
_flag: bool = False
# Development/etc flag
_ignore: bool = False

if _ignore is True:  # pyright: ignore[reportUnnecessaryComparison] # Purely for template branch.
    sys.exit(1)

# Grab Version from __init__.py
version = ""
with Path().joinpath(f"{project_name}/__init__.py").open() as file:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type:ignore

if not version:
    raise RuntimeError("Version is not set")


cl_file: pathlib.Path = pathlib.Path().joinpath("CHANGELOG.md")
if cl_file.exists() is False:
    msg = "Unable to locate the file. %s"
    raise FileNotFoundError(msg, cl_file.as_posix())


# Grab Version from `CHANGELOG.md`
# Searches for the first `# Version - X.Y.Z - [hash](url)` line
# instead of assuming it's always on line 0.
with cl_file.open(encoding="utf-8") as changelog:
    changelog_data = changelog.read()
    split_data = changelog_data.split("\n")

    ver_line: str | None = None
    for line in split_data:
        # Older changelogs wrote `## Version -`, newer ones `# Version -`.
        if line.lstrip("#").startswith(" Version -"):
            ver_line = line
            break

    if ver_line is not None:
        ver_parts = ver_line.split(" ")
        last_commit: str = ver_parts[-1][1:8]
        cl_ver: str = ver_parts[-3]
    else:
        # No version header found, treat it as an initial commit.
        last_commit = ""
        cl_ver = "0.0.0"

# If the version is `0.0.0` we are initializing the repo.
if cl_ver == "0.0.0":
    _flag = True

# Compare CHANGELOG.md and __init__.py Versions.
if _flag is False and (not version or cl_ver == version):
    msg = "<%s> | Version has not been updated `%s`: %s == `CHANGELOG.md`: %s"
    raise ValueError(msg, "Changelog Generator", gitHub_repo_name, version, cl_ver)


def gitHub_commit() -> None:
    # Verify that the current branch is `project_branch`.
    # `git branch` lists alphabetically, so its first line is not always the current branch.
    output: bytes = subprocess.check_output(["git", "branch", "--show-current"])
    branch: str = output.decode("utf-8").strip()
    if branch != project_branch:
        msg = "<%s> | Current branch is not `%s`: %s"
        raise RuntimeError(msg, "Changelog Generator", project_branch, branch)

    # Verify that there are new commits.
    output = subprocess.check_output(["git", "log"])
    new_commit = output.decode("utf-8").split("\n")[0][7:14]
    if new_commit == last_commit:
        msg = "No new commits since last version: %s == %s"
        raise RuntimeError(msg, last_commit, new_commit)

    # Format the git log data into a dictionary for Changelog.
    output = subprocess.check_output(["git", "log", "--format=%B", last_commit + "..HEAD"])
    files: dict[str, list[str]] = {}
    cur_data = output.decode("utf-8")
    cur_data = cur_data.strip()
    cur_data = cur_data.split("\n")
    file_name = None
    for entry in cur_data:
        _entry = entry
        if len(entry) == 0 or len(entry) == 1:
            continue
        if entry.startswith("$"):
            # This should skip our auto generated changelog commit from Github Actions.
            continue

        if entry.startswith("#"):
            file_name = entry[1:].strip()
            if file_name not in files:
                files[file_name] = []

        else:
            if entry.startswith("--"):
                _entry = "\t-" + entry[2:]
            if file_name is None:
                file_name = "Overall"
                files[file_name] = []
            files[file_name].append(_entry)

    update_changelog(version=version, new_commit=new_commit, files=files)


def gitHub_initial_commit() -> None:
    # Verify that there are new commits.
    output = subprocess.check_output(["git", "log"])
    new_commit = output.decode("utf-8").split("\n")[0][7:14]
    if new_commit == last_commit:
        msg = "No new commits since last version: %s == %s"
        raise RuntimeError(msg, last_commit, new_commit)

    # Format the git log data into a dictionary for Changelog.
    output = subprocess.check_output(["git", "log", "--format=%B"])
    files: dict[str, list[str]] = {}
    cur_data = output.decode("utf-8")
    cur_data = cur_data.strip()
    cur_data = cur_data.split("\n")
    file_name = None
    for entry in cur_data:
        _entry = entry
        if len(entry) == 0 or len(entry) == 1:
            continue
        if entry.startswith("$"):
            # This should skip our auto generated changelog commit from Github Actions.
            continue

        if entry.startswith("#"):
            file_name = entry[1:].strip()
            if file_name not in files:
                files[file_name] = []

        else:
            if entry.startswith("--"):
                _entry = "\t-" + entry[2:]
            if file_name is None:
                file_name = "Overall"
                files[file_name] = []
            files[file_name].append(_entry)

    update_changelog(version=version, new_commit=new_commit, files=files)


def update_changelog(version: str, new_commit: str, files: dict[str, list[str]]) -> None:
    # Format the data into the `CHANGELOG.md`
    set_version = f"# Version - {version} - [{new_commit[:7]}]({repo_url}/commit/{new_commit})\n"
    data = set_version
    for file_name, file_changes in files.items():
        data: str = data + "##" + file_name + "\n" + "\n".join(file_changes) + "\n\n"

    data = data + changelog_data
    with cl_file.open("r+", encoding="utf-8") as changelog:
        changelog.seek(0)
        changelog.truncate()
        changelog.write(data)


if _flag is True:
    gitHub_initial_commit()
else:
    gitHub_commit()

# Github Actions Checkout/Commit
# id | k8thekat = 68672235
subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=False)
subprocess.run(["git", "config", "user.email", "68672235+github-actions[bot]@users.noreply.github.com"], check=False)
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", f"$ Autogenerated Changelog for {version}"], check=False)
subprocess.run(["git", "push", "--force"], check=False)
