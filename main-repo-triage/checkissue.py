import json

import github
import github.Issue
import semver

with open("strings.json", encoding="utf8") as stringsfile:
    strings = json.load(stringsfile)

with open("template_titles.json", encoding="utf8") as templatetitlesfile:
    template_titles = json.load(templatetitlesfile)

# Load environmernt headings
with open("environment_titles.json", encoding="utf8") as envtitlesfile:
    env_titles = json.load(envtitlesfile)


def checkissue(i: github.Issue.Issue) -> str | None:
    """Validate a GitHub issue against template guidelines and version requirements.

    Inspect the issue's title and body to verify that all required sections are present
    (e.g., template titles, environment details, logs). Validate the version using
    semantic versioning, check for template alterations, and verify ffmpeg log formats.
    If discrepancies are found, return a formatted comment string with feedback;
    otherwise, return None.

    Parameters
    ----------
    i : github.Issue.Issue
        The GitHub issue object to validate.

    Returns
    -------
    Optional[str]
        A comment string  if the issue violates guidelines,
        or None if all checks pass.
    """

    # Check for empty title
    comment_string = [strings["header"]]
    print(f"[Debug] Title: {i.title}")
    print(f"[Debug] Body:  {i.body}")
    if i.title.strip().lower() == "[issue]:":
        comment_string.append(f"- {strings['empty_title']}")

    # Check for template format
    if not all(title in i.body for title in template_titles):
        comment_string.append(f"- {strings['invalid_template']}")
    else:
        body = i.body.splitlines()
        ptr = 0

        # Check version
        ptr = body.index("### Jellyfin Version") + 2
        version = body[ptr]
        # TODO: use proper version checking and comparison
        # Check if running unstable
        if version not in ("Master branch", "Weekly unstable"):
            try:
                version = semver.Version.parse(version)
                if version < semver.Version.parse("10.9.0"):
                    comment_string.append(f"- {strings['old_version']}")
            except ValueError:
                comment_string.append(f"- {strings['old_version']}")

        # Check Environment Section
        ptr = body.index("### Environment") + 3
        line = body[ptr]
        altered = False
        filled = True
        iis = False
        for offset, title in enumerate(env_titles):
            line = body[ptr + offset]
            if not line.startswith(title):
                altered = True
                break
            if len(line.strip()) == len(title):
                filled = False
                break
            if "iis" in line.lower():
                iis = True

        if altered:
            comment_string.append(f"- {strings['environment_altered']}")
        elif not filled:
            comment_string.append(f"- {strings['environment_not_filled']}")

        if iis:
            comment_string.append(f"- {strings['using_microsoft_iis']}")

        # Check Jellyfin Logs
        jflog_lines = 0
        ptr = body.index("### Jellyfin logs") + 3
        while line != "```":
            line = body[ptr]
            jflog_lines += 1
            ptr += 1

        if jflog_lines < 10:
            # comment_string.append('- ' + strings['too_few_logs'])
            pass

        # Check ffmpeg logs
        ptr = body.index("### FFmpeg logs") + 2
        if body[ptr] == "```shell":
            # ffmpeg log provided, check if valid
            line = body[ptr + 8]
            if not line.startswith("ffmpeg version"):
                comment_string.append(f"- {strings['invalid_ffmpeg_log']}")
            elif "-Jellyfin Copyright (c)" not in line:
                comment_string.append(f"- {strings['not_jellyfin_ffmpeg']}")
        else:
            # ffmpeg log not provided
            # comment_string.append('- ' + strings['no_ffmpeg_log'])
            pass

    # Make Comment
    comment_string.append("\n" + strings["footer"])
    print(f"[Debug] Raw Result: {comment_string}")
    if len(comment_string) > 2:
        comment_string = "\n".join(comment_string)
        return comment_string

    return None


def remove_top_checklist(i: github.Issue.Issue) -> None:
    """Remove the top checklist from a GitHub issue.

    Search for and remove a predefined checklist from the top of the issue body.
    After removal, trim any leading blank lines and update the issue body with the
    cleaned text.

    Parameters
    ----------
    i : github.Issue.Issue
        The GitHub issue object from which to remove the checklist.
    """

    LINES_LIST = [  # noqa: N806
        "### This issue respects the following points:",
        "- [X] This is a **bug**, not a question or a configuration issue; Please visit our [forum or chat rooms](https://jellyfin.org/contact/) first to troubleshoot with volunteers, before creating a report.",  # noqa: E501
        "- [X] This issue is **not** already reported on [GitHub](https://github.com/jellyfin/jellyfin/issues?q=is%3Aopen+is%3Aissue) _(I've searched it)_.",  # noqa: E501
        "- [X] I'm using an up to date version of Jellyfin Server stable, unstable or master; We generally do not support previous older versions. If possible, please update to the latest version before opening an issue.",  # noqa: E501
        "- [X] I agree to follow Jellyfin's [Code of Conduct](https://jellyfin.org/docs/general/community-standards.html#code-of-conduct).",
        "- [X] This report addresses only a single issue; If you encounter multiple issues, kindly create separate reports for each one.",  # noqa: E501
    ]

    body_lower_lines = i.body.lower().splitlines()
    body_lines = i.body.splitlines()

    for line in LINES_LIST:
        line_lower = line.lower()
        if line_lower in body_lower_lines:
            idx = body_lower_lines.index(line_lower)
            body_lower_lines.pop(idx)
            body_lines.pop(idx)
            print(f"[DBG]: Found line '{line}'")
        else:
            print(f"[DBG]: Line not found: '{line}'")
            break
    else:
        print("[INF]: Removing blank lines from top of template")
        while not body_lines[0]:
            body_lines.pop(0)
        i.edit(body="\n".join(body_lines))
