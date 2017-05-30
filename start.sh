#!/bin/bash

envsubst < /.sopel/default.cfg.tpl > /.sopel/default.cfg
exec sopel