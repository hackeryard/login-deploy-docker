#!/bin/bash

# create database
# using mysql docker container

export LOGINSERVER_CONF_FILE=`pwd`/loginserver_config.ini
echo ${LOGINSERVER_CONF_FILE}
 
# using env to subtitude
#HOSTNAME="192.168.48.136"
#PORT="3306"
#USERNAME="root"
#PASSWORD="password"
source mysql_config.ini

DBNAME="open_paas"
 
MYSQL_CMD="mysql -h${HOSTNAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD}"
echo ${MYSQL_CMD}

echo "create database ${DBNAME}"
create_db_sql="create database IF NOT EXISTS ${DBNAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci"
echo ${create_db_sql}  | ${MYSQL_CMD}
if [ $? -ne 0 ]
then
 echo "create databases ${DBNAME} failed ..."
 exit 1
fi

# 进入bin目录 执行数据库初始化
loginserver_install_dir='/root/loginserver-docker'
export LOGINSERVER_CONF_FILE=`pwd`/loginserver_config.ini
cd $loginserver_install_dir && python manage.py migrate
