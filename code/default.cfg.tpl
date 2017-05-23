[core]
nick = ${IRC_NICK} 
host = ${IRC_HOST}
use_ssl = false
port = ${IRC_PORT}
owner = ${IRC_OWNER}
channels = ${IRC_CHANS}
admins = ${IRC_ADMINS}
exclude = ${EXCLUDE_MODULES}
extra = ${SOPEL_EXTRA}
reply_errors = true

[admin]
hold_ground = true
auto_accept_invite = false


[twitter]
consumer_key = ${TWITTER_KEY}
consumer_secret = ${TWITTER_SECRET}