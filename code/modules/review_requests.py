import json
import sys
import requests
from sopel.module import commands, NOLIMIT, example, rule, rate
from sopel import web, tools
from sopel.formatting import colors, color, bold, underline
import sched
import time

projects = [
  "fabric8",
  "camel",
  "hawtio",
  "fuse",
  "cxf",
  "fuseenterprise",
  "karaf",
  "aries",
  "felix"
]



# curl -H 'Accept: application/vnd.github.black-cat-preview+json' -H 'Authorization: token 3799204db0aeac1cd0c25ec8a5526d8c63381f7c' https://api.github.com/repos/jboss-fuse/camel/pulls
# .url
# .state == open
# .locked == false
# 
# curl -H 'Accept: application/vnd.github.black-cat-preview+json' -H 'Authorization: token 3799204db0aeac1cd0c25ec8a5526d8c63381f7c' https://api.github.com/repos/jboss-fuse/camel/pulls/142/reviews
# 
# if( output empty then post)


base_url = "https://api.github.com"
token = '3799204db0aeac1cd0c25ec8a5526d8c63381f7c'
pulls_url = base_url + "/repos/jboss-fuse/:project/pulls"
single_pull_url = pulls_url + '/:pull/reviews'

headers = {
  'Accept': 'application/vnd.github.black-cat-preview+json',
  'Authorization': 'token 3799204db0aeac1cd0c25ec8a5526d8c63381f7c'
}

def query_jira(jira_id):
  response = requests.get(jboss_org_rest + jira_id, headers=headers)
  response = response.json()
  if "fields" in response:
    return "[{0}] {1} - {2}".format(jira_id, response["fields"]["summary"], color(jboss_org_case + jira_id , colors.GREY))
    color(text, colors.PINK) 
  else:
    return "Sorry but I couldn't fetch the URL"

@commands('pr')
@example('.pr')
@rate(600)
def pr(bot, trigger):
    #text = trigger.group(2)
    for project in projects:
        url = pulls_url.replace(':project', project)
        # print "[PR URL] " + url
        response = requests.get(url, headers=headers)
        prs = response.json()
        for pr in prs:
            if pr["state"] == "open" and pr["locked"] == False :
                pr_url = pr["url"]
                pr_html_url = pr["html_url"]
                pr_number = pr["number"]
                url = single_pull_url.replace(':project', project).replace(':pull', str(pr_number))
                # print "[PR reviews] " + url
                response = requests.get(url, headers=headers)
                response = response.json()
                # print  response
                if len(response) == 0:
                    bot.say( "[Approval Required] {0} - {1} - {2}".format(pr_html_url, pr["user"]["login"], color(pr["title"], colors.GREY)))


