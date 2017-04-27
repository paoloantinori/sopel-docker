#!/bin/bash
sudo -E -u sopel envsubst < /home/sopel/.sopel/default.cfg.tpl > /home/sopel/.sopel/default.cfg
sudo -u sopel sopel