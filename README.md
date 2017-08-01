# Sopel IRC bot Docker config

Run the Sopel IRC bot in a Docker container.

The image define a user since Sopel on its own, stops itself if it finds it's running as `root`.
This have some issue in multitenant manged environments like Openshift, and this is the reason why the `Dockerfile` is quite clumsy.

The image can be also run locally.
You can see it defines a set of environment variables, that are used to create a static config file at start up time.

```
IRC_NICK=bot_fuse_maintenance \
IRC_HOST=irc.devel.redhat.com \
IRC_PORT=6667 \
IRC_OWNER=paolo \
IRC_ADMINS=paolo \
IRC_CHANS="#fusesustaining" \
SOPEL_EXTRA=${_HOME}/.sopel/modules \
EXCLUDE_MODULES=adminchannel,announce,calc,clock,currency,dice,etymology,ip,lmgtfy,ping,rand,reddit,safety,search,tld,unicode_info,units,uptime,url,version,weather,ipython \
TWITTER_KEY=key \
TWITTER_SECRET=secret \
GH_TOKEN=secret
```

##### run in pure docker

```
docker run --rm \
  -e IRC_NICK=bot_the_second \
  -e IRC_HOST=127.0.0.1 \
  -e GH_TOKEN=XXXXXXX \
  pantinor/sopel-docker
```

##### run on openshift
```
oc delete all -l app=sopel
oc delete all -l app=ultrahook

oc new-build --name ultrahook-is -l app=sopel https://github.com/paoloantinori/ultrahook_alpine
oc new-build --name sopeldocker-is -l app=sopel https://github.com/paoloantinori/sopel-docker#os

oc new-app -l app=sopel ultrahook-is sopeldocker-is \
  --allow-missing-imagestream-tags \
  --group ultrahook-is+sopeldocker-is \
  --name sopeldocker \
  TWITTER_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  TWITTER_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  GH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  ULTRAHOOK_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  ULTRAHOOK_TARGET_PORT=http://localhost:8080 \
  ULTRAHOOK_DOMAIN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

oc patch dc sopeldocker --type='json' -p='[{"op": "replace", "path": "/spec/strategy", "value":{"type": "Recreate", "recreateParams": { } } }]'
oc set resources dc sopeldocker -c=sopeldocker --limits=cpu=500m,memory=50Mi --requests=cpu=100m,memory=50Mi
oc set resources dc sopeldocker -c=sopeldocker-1 --limits=cpu=500m,memory=256Mi --requests=cpu=100m,memory=256Mi

WEB_HOOK_ENDPOINT=$(oc describe bc sopeldocker-is | grep -A 1 "Webhook GitHub" | tail -n1 | grep --color=never --only-matching 'http.*')

oc new-app -l app=ultrahook ultrahook-is \
  ULTRAHOOK_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  ULTRAHOOK_TARGET_PORT="$WEB_HOOK_ENDPOINT" \
  ULTRAHOOK_DOMAIN=YYYYYYYYYYYYYYYYYYYYYYYYY

oc set resources dc ultrahook-is --limits=cpu=500m,memory=50Mi --requests=cpu=100m,memory=50Mi
```