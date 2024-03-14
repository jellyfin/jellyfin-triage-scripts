import github
import datetime

from checkissue import checkissue

# Read token
with open('token.txt', 'r', encoding='utf8') as tokenfile:
    TOKEN = tokenfile.read().strip()

auth = github.Auth.Token(TOKEN)
gh = github.Github(auth=auth)

# Get input
ISSUE = int(input("Please enter issue number: "))
REPO = "jellyfin/jellyfin"

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

if res:
    issue.create_comment(res)