from sopel.formatting import colors, color, bold, underline
from sopel.module import commands, NOLIMIT, example, rule, rate
from threading import Thread
import json
import logging
import os
import requests
import sched
import sys
import time
import traceback
import web


channels = [
  "#paolo",
  "#fusesustaining"
  ]

projects = [
  "aries",
  "camel",
  "cxf",
  "fabric8",
  "felix",
  "fuse",
  "fuseenterprise",
  "fuse-eap",
  "hawtio",
  "karaf",
  "perfectus",
  "quickstarts-ops",
  "wildfly-camel",
  "fuse-karaf"
]

bot_instance = None

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


urls = (
  # the second param here is a Class
  '/', 'webhook',
  '/hello', 'index'
)

class index:
    logger = logging.getLogger(__name__)
    def GET(self):
        # print bot_instance
        logger.info("Hello, world!")
        for channel in channels:
            bot_instance.say("message", channel)
        return ""
class webhook:
    logger = logging.getLogger(__name__)
    def POST(self):
        logger.info ("web hook invoked")
        data = web.data()
        message = inspect_event(data)
        for channel in channels:
            bot_instance.say(message, channel)
        logger.info ("Webhook data:" + data)
# listen on port 8080
app = web.application(urls, globals())
server = Thread(target=app.run)
server.setDaemon(True)
server.start()

def inspect_event(event_string):
    message = ""
    event = json.loads(event_string)
    if "action" in event:
        logger.info ("Action is: " + event["action"])
    if "pull_request" in event:
        logger.info ("it's a pull request")
        url = event["pull_request"]["_links"]["html"]["href"]
        user = event["sender"]["login"].decode('unicode-escape').encode("utf-8")
        title = event["pull_request"]["title"].decode('unicode-escape').encode("utf-8")
        if event["action"] in ["review_requested", "opened", "reopened"]:
            logger.info ("it's an open")
            message = "[Approval Required] {0} - {1} - {2}".format(url, user, color(title, colors.GREY))
        elif event["action"] in ["closed"]:
            logger.info ("it's a closed")
            message = "[Closed] {0} - {1} - {2}".format(url, user, color(title, colors.GREY))
        elif event["action"] in ["submitted"]:
            logger.info ("it's a review")
            if "review" in event:
                commenter = event["review"]["user"]["login"].decode('unicode-escape').encode("utf-8")
                url = event["review"]["html_url"]
                state = event["review"]["state"]
                if "approved" == state:
                    message = "[Approved by {0}] {1} - {2} - {3}".format(commenter ,url, user, color(title, colors.GREY) )
                elif "commented" == state:
                    body = event["review"]["body"]
                    message = "[Commented by {0}] {1} - {2} - {3}: {4}".format(commenter ,url, user, color(title, colors.GREY), body.decode('unicode-escape').encode("utf-8") )
                else:
                    logger.warning ("NEED TO STUDY THIS EXECUTION BRANCH")
    else:
        logger.warning ("it's something else")
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
    logger.info ("\ninvoking setup\n")
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
    bot.say( "Looking for PRs. Hold on a second...")
    #text = trigger.group(2)
    tot = 0
    
    for project in projects:
        url = pulls_url.replace(':project', project)
        # logger.info "[PR URL] " + url
        try:
            response = requests.get(url, headers=headers)
            prs = response.json()
            for pr in prs:
                logger.info (pr)
                if pr["state"] == "open" and pr["locked"] == False :
                    pr_url = pr["url"]
                    pr_html_url = pr["html_url"]
                    pr_number = pr["number"]
                    url = single_pull_url.replace(':project', project).replace(':pull', str(pr_number))
                    # logger.info "[PR reviews] " + url
                    try:
                        response = requests.get(url, headers=headers)
                        response = response.json()
                        # logger.info  response
                        if len(response) == 0:
                            tot = tot+1
                            user = pr["user"]["login"].decode('unicode-escape').encode("utf-8")
                            title = pr["title"].decode('unicode-escape').encode("utf-8")
                            bot.say( "[Approval Required] {0} - {1} - {2}".format(pr_html_url, user, color(title, colors.GREY)))
                    except Exception as e:
                        logger.error (traceback.format_exc())
                        bot.say( "Error invoking {0}".format(url))
        except Exception as e:
            logger.error ( traceback.format_exc())
            bot.say( "Error invoking {0}".format(url))
    if tot == 0:
        bot.say( "[No pending PRs]")

