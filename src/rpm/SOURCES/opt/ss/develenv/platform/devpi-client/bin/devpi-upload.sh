#!/bin/bash
source /etc/sysconfig/develenv-devpi-client
DEVPI_COMMAND=$DEVPI_CLIENT_HOME/bin/devpi
DEVPI_PYTHONPATH=$DEVPI_CLIENT_HOME/lib:${PYTHONPATH}
PYTHONPATH=${DEVPI_PYTHONPATH} $DEVPI_COMMAND use http://${DEVPI_HOSTNAME}/devpi/develenv/dev
PYTHONPATH=${DEVPI_PYTHONPATH} $DEVPI_COMMAND login develenv --password=develenv
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
PYTHONPATH=${DEVPI_PYTHONPATH} $DEVPI_COMMAND upload -p $(grep -Po "(?<=#\!).*" setup.py) --no-vcs
