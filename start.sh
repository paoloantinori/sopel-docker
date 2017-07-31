#!/bin/bash

envsubst < ${HOME}/.sopel/default.cfg.tpl > ${HOME}/.sopel/default.cfg
exec sopel