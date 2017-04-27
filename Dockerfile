FROM fedora:25
MAINTAINER Paolo Antinori

RUN useradd -m -d /home/sopel sopel
WORKDIR /home/sopel

RUN dnf update -y && \
    dnf install -y git python3-enchant gettext

RUN pip3 install git+https://github.com/sopel-irc/sopel.git

COPY scripts/ /tmp/scripts
COPY start.sh /
# this convoluted thing is because of issues to perform `chown` across multiple commands
RUN chmod a+rx /start.sh &&\
    rm -rf /home/sopel/.sopel &&\
    mkdir -p /home/sopel/.sopel &&\
    cp -R /tmp/scripts/* /home/sopel/.sopel &&\
    chown -R sopel:sopel /home/sopel &&\
    rm -rf /tmp/scripts
# VOLUME /home/sopel/.sopel

USER sopel
CMD /start.sh

ENV LANG en_US.UTF-8

ENV IRC_NICK bot_fuse_maintenance
ENV IRC_HOST irc.devel.redhat.com

ENV IRC_PORT 6667
ENV IRC_OWNER paolo
ENV IRC_ADMINS paolo
ENV IRC_CHANS "#fusesustaining"
#ENV reply_errors = false
ENV SOPEL_EXTRA	/home/sopel/.sopel/modules
ENV EXCLUDE_MODULES adminchannel,announce,calc,clock,currency,dice,etymology,ip,lmgtfy,ping,rand,reddit,safety,search,tell,tld,unicode_info,units,uptime,url,version,weather

ENV TWITTER_KEY key
ENV TWITTER_SECRET secret


