import json
import sys
import requests
from sopel.module import commands, NOLIMIT, example, rule
from sopel import web, tools
from sopel.formatting import colors, color, bold, underline

if sys.version_info.major < 3:
  from urllib2 import HTTPError
  from urlparse import urlparse
else:
  from urllib.request import HTTPError
  from urllib.parse import urlparse

# https://issues.jboss.org/rest/api/2/issue/ENTESB-6449
jboss_org_base_url = "https://issues.jboss.org"
jboss_org_rest = jboss_org_base_url + "/rest/api/2/issue/"
jboss_org_case = jboss_org_base_url + "/browse/"

def query_jira(jira_id):
  response = requests.get(jboss_org_rest + jira_id)
  response = response.json()
  if "fields" in response:
    return "[{0}] {1} - {2}".format(jira_id, response["fields"]["summary"], color(jboss_org_case + jira_id , colors.GREY))
  else:
    return "Sorry but I couldn't fetch the URL"

@rule('.*(ENTESB-\d+).*')
def versions(bot, trigger):
  text = trigger.group(1)
  bot.say( query_jira(text) )

