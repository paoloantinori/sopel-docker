from sopel.formatting import colors, color, bold, underline
from sopel.module import commands, NOLIMIT, example, rule, rate
from threading import Thread
import json
import os
import requests
import sched
import sys
import time
import web

channels = [
  "#paolo",
  "#fusesustaining"
  ]

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

bot_instance = None


urls = (
  # the second param here is a Class
  '/', 'webhook',
  '/hello', 'index'
)

class index:
    def GET(self):
        # print bot_instance
        print ("Hello, world!")
        for channel in channels:
            bot_instance.say("message", channel)
        return ""
class webhook:
    def POST(self):
        print ("web hook invoked")
        data = web.data()
        message = inspect_event(data)
        for channel in channels:
            bot_instance.say(message, channel)
        print (data)
# listen on port 8080
app = web.application(urls, globals())
server = Thread(target=app.run)
server.setDaemon(True)
server.start()

def inspect_event(event_string):
    message = ""
    event = json.loads(event_string)
    if "pull_request" in event:
        print ("it's a pull request")
        if "review_requested" == event["action"]:
            message = "NEW Review Request: " + event["_links"]["html"]
    else:
        print ("it's something else")
    return message

# curl -H 'Accept: application/vnd.github.black-cat-preview+json' -H 'Authorization: token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' https://api.github.com/repos/jboss-fuse/camel/pulls
# .url
# .state == open
# .locked == false
# 
# curl -H 'Accept: application/vnd.github.black-cat-preview+json' -H 'Authorization: token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' https://api.github.com/repos/jboss-fuse/camel/pulls/142/reviews
# 
# if( output empty then post)


def setup(bot):
    print ("\ninvoking setup\n")
    global bot_instance
    bot_instance = bot

def configure(config):
    config.core

base_url = "https://api.github.com"
token = os.environ['GH_TOKEN']
pulls_url = base_url + "/repos/jboss-fuse/:project/pulls"
single_pull_url = pulls_url + '/:pull/reviews'

headers = {
  'Accept': 'application/vnd.github.black-cat-preview+json',
  'Authorization': 'token ' + token
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
            print (pr)
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


