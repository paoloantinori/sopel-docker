# centos/python-35-centos7
FROM openshift/base-centos7

MAINTAINER Paolo Antinori <pantinor@redhat.com>

LABEL io.k8s.description="Platform for building Sopel IRC bots" 
#LABEL io.openshift.s2i.destination=/tmp/src
LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

RUN yum install -y epel-release && yum install -y git python-enchant nss_wrapper gettext python-pip && yum clean all -y
RUN pip install web.py git+https://github.com/sopel-irc/sopel.git

COPY ./s2i/bin/ /usr/libexec/s2i

# COPY ./scripts/modules /opt/app-root/src/.sopel
# COPY ./scripts /opt/app-root/src
# COPY start.sh /opt/app-root
# RUN chmod +x /opt/app-root/start.sh && chown -R 1001:1001 /opt/app-root

USER 1001
WORKDIR /opt/app-root

CMD ["/usr/libexec/s2i/usage"]

ENV LANG=en_US.UTF-8 \
    IRC_NICK=bot_fuse_maintenance \
    IRC_HOST=irc.devel.redhat.com \
    IRC_PORT=6667 \
    IRC_OWNER=paolo \
    IRC_ADMINS=paolo \
    IRC_CHANS="#fusesustaining" \
    SOPEL_EXTRA=/opt/app-root/src/.sopel \
    EXCLUDE_MODULES=adminchannel,announce,calc,clock,currency,dice,etymology,ip,lmgtfy,ping,rand,reddit,safety,search,tld,unicode_info,units,uptime,url,version,weather \
    TWITTER_KEY=key \
    TWITTER_SECRET=secret