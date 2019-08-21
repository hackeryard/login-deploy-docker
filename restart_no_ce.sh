#!/bin/bash
set -x

# config HYDRA
LOGIN_PROVIDER_IP_PORT=10.10.26.22:3001
HYDRA_ISSUER_IP=10.10.26.22
HYDRA_ISSUER_PORT=4443

#config LOGINSERVER
LOGINSERVER_IP=10.10.26.22
LOGINSERVER_PORT=8003


echo "stoping all..."

ps -ef | grep hydra | awk '{print $2}' | xargs kill -9
ps -ef | grep consent | awk '{print $2}' | xargs kill -9
ps -ef | grep manage | awk '{print $2}' | xargs kill -9

sleep 3

echo "starting all"

echo "starting hydra"
export OAUTH2_CONSENT_URL=http://${LOGIN_PROVIDER_IP_PORT}/consent
export OAUTH2_LOGIN_URL=http://${LOGIN_PROVIDER_IP_PORT}/login
export OAUTH2_ISSUER_URL=http://${HYDRA_ISSUER_IP}:${HYDRA_ISSUER_PORT}
export OAUTH2_SHARE_ERROR_DEBUG=1
export LOG_LEVEL=debug
export DATABASE_URL=postgres://hydra:secret@localhost:5432/hydra?sslmode=disable
export SYSTEM_SECRET=fdfdsearas92jj3x
export PUBLIC_PORT=${HYDRA_ISSUER_PORT}

nohup ./hydra serve all --dangerous-force-http > hydra.log 2>&1 &


echo "starting login-consent"
export NODE_CONF_FILE=node_config.ini 
nohup ./hydra-identity-and-consent-provider-node > login-consent.log 2>&1 &

echo "starting loginserver"
export LOGINSERVER_CONF_FILE=loginserver_config.ini
dh_venv_install_dir='/opt/venvs/loginserver'
cd $dh_venv_install_dir/bin && source activate && nohup ./python manage.py runserver ${LOGINSERVER_IP}:${LOGINSERVER_PORT} > loginserver.log 2>&1 &
