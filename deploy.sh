#!/bin/bash
set -x

source hydra_config.ini

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
export LOGINSERVER_CONF_FILE=`pwd`/loginserver_config.ini
loginserver_install_dir='/root/loginserver-docker'
cd $loginserver_install_dir && nohup python manage.py runserver ${LOGINSERVER_IP}:${LOGINSERVER_PORT} > loginserver.log 2>&1 &

echo "please wait 15 seconds"
sleep 15

#./create_grafana_client.sh && ./create_loginserver_client.sh

./hydra clients create \
--endpoint http://${HYDRA_ISSUER_IP}:4445 \
--id test-client-grafana \
--secret test-secret-grafana \
--response-types code,id_token \
--grant-types refresh_token,authorization_code \
--scope openid,offline \
--callbacks http://${GRAFANA_IP}:${GRAFANA_PORT}/grafana/login/generic_oauth

./hydra clients create \
--endpoint http://${HYDRA_ISSUER_IP}:4445 \
--id test-client \
--secret test-secret \
--response-types code,id_token \
--grant-types refresh_token,authorization_code \
--scope openid,offline \
--token-endpoint-auth-method client_secret_post \
--callbacks http://${LOGINSERVER_IP}:${LOGINSERVER_PORT}/

