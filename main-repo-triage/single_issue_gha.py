import github
import datetime
import os

from checkissue import checkissue, remove_top_checklist

# Read token
TOKEN = os.getenv("GH_TOKEN")
auth = github.Auth.Token(TOKEN)
gh = github.Github(auth=auth)

# see if testing environment
TESTING = os.getenv("TESTING") == 'True'

# Get input
ISSUE = int(os.getenv("ISSUE"))
REPO = os.getenv("GH_REPO")

# with open('strings.json', 'r', encoding='utf8') as stringsfile:
#     strings = json.load(stringsfile)

# with open('template_titles.json', 'r', encoding='utf8') as templatetitlesfile:
#     template_titles = json.load(templatetitlesfile)

# Load environmernt headings
# with open('environment_titles.json', 'r', encoding='utf8') as envtitlesfile:
#     env_titles = json.load(envtitlesfile)

repo = gh.get_repo(REPO)
issue = repo.get_issue(ISSUE)
        
res = checkissue(issue)
print(res)

# Inhibit Until I have time to modify for new template

if res and TESTING:
    pass
    # issue.create_comment(res)

print('[INF]: Removing checklist')
remove_top_checklist(issue)
