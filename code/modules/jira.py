import json
import sys
import requests
from sopel.module import commands, NOLIMIT, example, rule
from sopel import web, tools
from sopel.formatting import colors, color, bold, underline

# https://issues.jboss.org/rest/api/2/issue/ENTESB-6449
jboss_org_base_url_dns = "https://issues.jboss.org"

# hack for rh ipaas
headers = {'Host': 'issues.jboss.org'}
jboss_org_base_url = "https://209.132.182.82"
# end hack

jboss_org_rest = jboss_org_base_url + "/rest/api/2/issue/"
jboss_org_case = jboss_org_base_url + "/browse/"


def query_jira(jira_id):
  url = jboss_org_rest + jira_id
  response = requests.get(url, headers=headers, verify=False)
  response = response.json()
  if "fields" in response:
    return "[{0}] {1} - {2}".format(jira_id, response["fields"]["summary"], color(jboss_org_case.replace(jboss_org_base_url,jboss_org_base_url_dns) + jira_id , colors.GREY))
  else:
    return "Sorry but I couldn't fetch the URL"

@rule('.*(ENTESB-\d+).*')
def versions(bot, trigger):
  text = trigger.group(1)
  bot.say( query_jira(text) )

