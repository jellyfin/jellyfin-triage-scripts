import github
import datetime

from checkissue import checkissue

# Read token
with open('token.txt', 'r', encoding='utf8') as tokenfile:
    TOKEN = tokenfile.read().strip()

auth = github.Auth.Token(TOKEN)
gh = github.Github(auth=auth)

try:
    with open('last_run.txt', 'r', encoding='utf8') as lastrunfile:
        raw = lastrunfile.read().strip()
        last_run = datetime.datetime.fromtimestamp(float(raw))
except:
    last_run = datetime.datetime.fromtimestamp(0)

try:
    with open('last_issue.txt', 'r', encoding='utf8') as lastissuefile:
        last_issue = int(lastissuefile.read.strip())
except:
    last_issue = 0

with open('last_run.txt', 'w', encoding='utf8') as lastrunfile:
    lastrunfile.write(str(datetime.datetime.now().timestamp()))

# with open('strings.json', 'r', encoding='utf8') as stringsfile:
#     strings = json.load(stringsfile)

# with open('template_titles.json', 'r', encoding='utf8') as templatetitlesfile:
#     template_titles = json.load(templatetitlesfile)

# Load environmernt headings
# with open('environment_titles.json', 'r', encoding='utf8') as envtitlesfile:
#     env_titles = json.load(envtitlesfile)

repo = gh.get_repo("felix920506/jellyfin")
issues = repo.get_issues(state='open', since=last_run)
last_issue_new = last_issue
for i in issues:
    # Ignore previously looked at issues
    if i.number > last_issue:
        if i.number > last_issue_new:
            last_issue_new = i.number
        
        # Check if someone else has commented
        other_comment = False
        comments = i.get_comments()
        for j in comments:
            if j.user.login != i.user.login:
                other_comment = True
                break
        
        if not other_comment:
            res = checkissue(i)

            if res:
                i.create_comment(res)
        

with open('last_issue.txt', 'w', encoding='utf8') as lastissuefile:
    lastissuefile.write(str(last_issue_new))