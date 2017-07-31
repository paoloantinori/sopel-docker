#!/bin/bash
printenv
envsubst < ${PWD}/.sopel/default.cfg.tpl > ${PWD}/.sopel/default.cfg
exec sopel