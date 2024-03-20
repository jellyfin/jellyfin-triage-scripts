# Jellyfin Triage Scripts

Part of the [Jellyfin](https://jellyfin.org) project.

## What is this?

This repo is intended for small tools and scripts used by the triage team to help triage and troubleshoot issues.

## Reporting issues

Report them in the issues sction

## Contributing guidelines

[Jellyfin contribution guidelines](https://jellyfin.org/docs/general/contributing) apply.

### Repo Specific things

- Tools should be written in cross platform languages that do not need to be compiled. Python, Javascript/Typescript or C# are the preferred languages.
- Each set of tools should be separated into its own subdirectory, with its own set of requirements and environment files.
- If a PR intends to add a new Github function, the PR where it is added to the intended repo should be linked.
- Please include ample amounts of comments, as people who are less experienced with coding may be working on the tools here.
- Please follow styling below.

### Styling

This section is for styling. When a linter is setup in the future, these guidelines will be setup as linter rules.

- Tab = 4 spaces
- If code is commented out, there should be comments explaining why said code was commented out.
- put \{ on the same line as the preceding statement, not on the next line.
- Follow language norms if not specified here.

### Tests

There are currently no tests written for this repo. PR for tests are welcome. Tests will start appearing when things start breaking.
