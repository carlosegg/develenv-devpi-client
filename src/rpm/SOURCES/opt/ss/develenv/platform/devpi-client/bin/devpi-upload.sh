#!/bin/bash
source /etc/sysconfig/develenv-devpi-client
export PYTHONPATH=$DEVPI_CLIENT_HOME/lib
DEVPI_COMMAND="$DEVPI_CLIENT_HOME/bin/devpi"
$DEVPI_COMMAND use http://${DEVPI_HOSTNAME}/devpi/develenv/dev
$DEVPI_COMMAND login develenv --password=develenv
if [[ -f setup.cfg ]]; then
   git add -f setup.cfg
fi
if [[ -f VERSION ]]; then
   git add -f VERSION
fi
# SCM_INFO contains url and hash of scm
if [[ -f SCM_INFO ]]; then
   git add -f SCM_INFO
fi
$DEVPI_COMMAND upload -p $(grep -Po "(?<=#\!).*" setup.py) --no-vcs
