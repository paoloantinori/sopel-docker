#!/bin/bash
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
cd /opt/app-root/src/.sopel
envsubst < passwd.tpl > /tmp/passwd
envsubst < default.cfg.tpl > default.cfg
export LD_PRELOAD=/usr/lib64/libnss_wrapper.so
export NSS_WRAPPER_PASSWD=/tmp/passwd
export NSS_WRAPPER_GROUP=/etc/group
exec sopel