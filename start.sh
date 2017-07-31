#!/bin/bash
printenv
envsubst < ${HOME}/.sopel/default.cfg.tpl > ${HOME}/.sopel/default.cfg
exec sopel