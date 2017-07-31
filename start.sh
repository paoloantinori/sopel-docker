#!/bin/bash
printenv
set -x
echo "Applying variables to config template"
envsubst < ${PWD}/.sopel/default.cfg.tpl > ${PWD}/.sopel/default.cfg
exec sopel