#!/bin/bash
set -x
echo "stoping all..."

ps -ef | grep hydra | awk '{print $2}' | xargs kill -9
ps -ef | grep consent | awk '{print $2}' | xargs kill -9
ps -ef | grep manage | awk '{print $2}' | xargs kill -9

sleep 3

echo "starting all"

echo "starting hydra"
nohup ./start_hydra_server_postgre.sh > hydra.log 2>&1 &

echo "starting login-consent"
export NODE_CONF_FILE=node_config.ini 
nohup ./hydra-identity-and-consent-provider-node > login-consent.log 2>&1 &

echo "starting loginserver"
export LOGINSERVER_CONF_FILE=loginserver_config.ini
dh_venv_install_dir='/opt/venvs/loginserver'
cd $dh_venv_install_dir/bin && source activate && nohup ./python manage.py runserver $1:8003 > loginserver.log 2>&1 &

echo "please wait 15 seconds"
sleep 15

./create_grafana_client.sh && ./create_loginserver_client.sh

