#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,getopt,os,shutil
from string import Template


class FileTemplate(Template):
    delimiter='$'

def generate_config_file(loginserver_ip,loginserver_port,hydra_ip,hydra_port,login_consent_ip,login_consent_port,grafana_ip,grafana_port,nginx_ip,nginx_port,mysql_hostname,mysql_port,mysql_username,mysql_password):

    # loginserver_config.ini
    loginserver_config_template_str='''# loginserver的配置文件
[server]
# 服务端口
port = $loginserver_port
# 服务模式(http, https)
http_schema = http
# cookie有效域
bk_cookie_domain = $loginserver_ip
# oauth 2.0 callback url
paas_domain = $loginserver_ip:$loginserver_port
# 日志级别
log_level = DEBUG
# 初始密码设定
[admin]
username = admin
password = admin
[oauth]
# oauth2.0 登录URL
login_url = http://$hydra_ip:$hydra_port/oauth2/auth
# 通过认证Code获取Access_token的API URL
token_url = http://$hydra_ip:$hydra_port/oauth2/token
# 获取用户信息的API URL
userinfo_url = http://$hydra_ip:$hydra_port/userinfo
# OAuth 2.0 客户端 ID
client_id = test-client
# OAuth 2.0 客户端 密钥
client_secret = test-secret
# 数据库设定
[database]
host = localhost
user = root
password = password
database = open_paas
port = 3306
'''
    template = FileTemplate(loginserver_config_template_str)
    result = template.substitute(dict(loginserver_ip=loginserver_ip,loginserver_port=loginserver_port,hydra_ip=hydra_ip,hydra_port=hydra_port))
    with open("loginserver_config.ini",'w') as tmp_file:
        tmp_file.write(result)


    # node_config.ini
    node_config_template_str='''# login和consent provider的配置文件
[server]
port = $login_consent_port
hydra_admin_url = http://$hydra_ip:4445
[remember]
login_remember = 300
consent_remember = 300
[database]
host = localhost
user = root
password = password
database = open_paas
'''
    template = FileTemplate(node_config_template_str)
    result = template.substitute(dict(login_consent_port=login_consent_port,hydra_ip=hydra_ip))
    with open("node_config.ini",'w') as tmp_file:
        tmp_file.write(result)


    # hydra_config.ini
    hydra_config_template_str='''# config HYDRA
LOGIN_PROVIDER_IP_PORT=$login_consent_ip:$login_consent_port
HYDRA_ISSUER_IP=$hydra_ip
HYDRA_ISSUER_PORT=$hydra_port
#config LOGINSERVER
LOGINSERVER_IP=$loginserver_ip
LOGINSERVER_PORT=$loginserver_port
#config grafana client
GRAFANA_IP=$grafana_ip
GRAFANA_PORT=$grafana_port
NGINX_IP=$nginx_ip
NGINX_PORT=$nginx_port
'''
    template = FileTemplate(hydra_config_template_str)
    result = template.substitute(dict(login_consent_ip=login_consent_ip,login_consent_port=login_consent_port,hydra_ip=hydra_ip,hydra_port=hydra_port,loginserver_ip=loginserver_ip,loginserver_port=loginserver_port,grafana_ip=grafana_ip,grafana_port=grafana_port,nginx_ip=nginx_ip,nginx_port=nginx_port))
    with open("hydra_config.ini",'w') as tmp_file:
        tmp_file.write(result)

    # mysql_config.ini
    mysql_config_template_str='''# config mysql
HOSTNAME=$mysql_hostname
PORT=$mysql_port
USERNAME=$mysql_username
PASSWORD=$mysql_password
'''
    template = FileTemplate(mysql_config_template_str)
    result = template.substitute(dict(mysql_hostname=mysql_hostname,mysql_port=mysql_port,mysql_username=mysql_username,mysql_password=mysql_password))
    with open("mysql_config.ini",'w') as tmp_file:
        tmp_file.write(result)


def main(argv):
    loginserver_port='8003'
    hydra_port='4443'
    login_consent_port='3001'
    grafana_port='3000'
    nginx_port='8089'
    mysql_username='root'
    mysql_port='3306'

    try:#need remove
        opts, _ = getopt.getopt(argv,"hd:D:r:p:x:s:m:P:X:S:u:U:a:l:"\
        ,["help","loginserver_ip=","loginserver_port=","hydra_ip=","hydra_port="\
        ,"login_consent_ip=","login_consent_port=","grafana_ip=","grafana_port=","nginx_ip=","nginx_port=","mysql_hostname=","mysql_port=","mysql_username=","mysql_password="])

    except getopt.GetoptError as e:
        print("\n \t",e.msg)
        print('''
    usage:
      --loginserver_ip          <loginserver_ip>          the loginserver ip, eg:10.10.26.24
      --loginserver_port        <loginserver_port>        the loginserver port, default 8003
      --hydra_ip                <hydra_ip>                the hydra ip, eg:10.10.26.24
      --hydra_port              <hydra_port>              the hydra issuer port, default:4443
      --login_consent_ip        <login_consent_ip>        the login-consent ip, eg:10.10.26.24
      --login_consent_port      <login_consent_port>      the login-conset port, default 3001
      --grafana_ip              <grafana_ip>              the grafana service ip, eg:10.10.26.24
      --grafana_port            <grafana_port>            the grafana service port, default 3000
      --nginx_ip                <nginx_ip>                the nginx reverse server ip
      --nginx_port              <nginx_port>              the nginx reverse server port, default 8089
      --mysql_hostame           <mysql_hostname>          the mysql servive for loginserver and consent
      --mysql_port              <mysql_port>
      --mysql_username          <mysql_username>
      --mysql_password          <mysql_password>
    ''')

        sys.exit(2)
    if len(opts) == 0:
        print('''
    usage:
      --loginserver_ip          <loginserver_ip>          the loginserver ip, eg:10.10.26.24
      --loginserver_port        <loginserver_port>        the loginserver port, default 8003
      --hydra_ip                <hydra_ip>                the hydra ip, eg:10.10.26.24
      --hydra_port              <hydra_port>              the hydra issuer port, default:4443
      --login_consent_ip        <login_consent_ip>        the login-consent ip, eg:10.10.26.24
      --login_consent_port      <login_consent_port>      the login-conset port, default 3001
      --grafana_ip              <grafana_ip>              the grafana service ip, eg:10.10.26.24
      --grafana_port            <grafana_port>            the grafana service port, default 3000
      --nginx_ip                <nginx_ip>                the nginx reverse server ip
      --nginx_port              <nginx_port>              the nginx reverse server port, default 8089
      --mysql_hostame           <mysql_hostname>          the mysql servive for loginserver and consent
      --mysql_port              <mysql_port>
      --mysql_username          <mysql_username>
      --mysql_password          <mysql_password>
    ''')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h','--help'):
            print('''
        usage:
        --loginserver_ip          <loginserver_ip>          the loginserver ip, eg:10.10.26.24
        --loginserver_port        <loginserver_port>        the loginserver port, default 8003
        --hydra_ip                <hydra_ip>                the hydra ip, eg:10.10.26.24
        --hydra_port              <hydra_port>              the hydra issuer port, default:4443
        --login_consent_ip        <login_consent_ip>        the login-consent ip, eg:10.10.26.24
        --login_consent_port      <login_consent_port>      the login-conset port, default 3001
        --grafana_ip              <grafana_ip>              the grafana service ip, eg:10.10.26.24
        --grafana_port            <grafana_port>            the grafana service port, default 3000
        --nginx_ip                <nginx_ip>                the nginx reverse server ip
        --nginx_port              <nginx_port>              the nginx reverse server port, default 8089
        --mysql_hostame           <mysql_hostname>          the mysql servive for loginserver and consent
        --mysql_port              <mysql_port>
        --mysql_username          <mysql_username>
        --mysql_password          <mysql_password>
    ''')
            sys.exit()
        elif opt in ("--loginserver_ip"):
            loginserver_ip=arg
            print('loginserver_ip:'+loginserver_ip)
        elif opt in ("--loginserver_port"):
            loginserver_port=arg
            print('loginserver_port:',loginserver_port)
        elif opt in ("--hydra_ip"):
            hydra_ip= arg
            print('hydra_ip:'+hydra_ip)
        elif opt in ("--hydra_port"):
            hydra_port = arg
            print('hydra_port:',hydra_port)
        elif opt in ("--login_consent_ip"):
            login_consent_ip = arg
            print('login_consent_ip:',login_consent_ip)
        elif opt in ("--login_consent_port"):
            login_consent_port = arg
            print('login_consent_port:',login_consent_port)
        elif opt in ("--grafana_ip"):
            grafana_ip = arg
            print('grafana_ip:',grafana_ip)
        elif opt in ("--grafana_port"):
            grafana_port = arg
            print('grafana_port:',grafana_port)
        elif opt in ("--nginx_ip"):
            nginx_ip = arg
            print('nginx_ip:',nginx_ip)
        elif opt in ("--nginx_port"):
            nginx_port = arg
            print('nginx_port:',nginx_port)
        elif opt in ("--mysql_hostname"):
            mysql_hostname = arg
            print('mysql_hostname:',mysql_hostname)
        elif opt in ("--mysql_port"):
            mysql_port = arg
            print('mysql_port:',mysql_port)
        elif opt in ("--mysql_username"):
            mysql_username = arg
            print('mysql_username:',mysql_username)
        elif opt in ("--mysql_password"):
            mysql_password = arg
            print('mysql_password:',mysql_password)

    if 0 == len(loginserver_ip):
        print('please input the loginserver ip, eg:10.10.26.24')
        sys.exit()
    if 0 == len(loginserver_port):
        print('please input the loginserver port, default 8003')
        sys.exit()
    if 0 == len(hydra_ip):
        print('please input the hydra ip, eg:10.10.26.24')
        sys.exit()
    if 0 == len(hydra_port):
        print('please input the hydra issuer port, default:4443')
        sys.exit()
    if 0 == len(login_consent_ip):
        print('please input the login-consent ip, eg:10.10.26.24')
        sys.exit()
    if 0 == len(login_consent_port):
        print('please input the login-conset port, default 3001')
        sys.exit()
    if 0 == len(grafana_ip):
        print('please input the grafana service ip, eg:10.10.26.24')
        sys.exit()
    if 0 == len(grafana_port):
        print('please input the grafana service port, default 3000')
        sys.exit()
    if 0 == len(nginx_ip):
        print('please input the nginx service ip, eg:10.10.26.24')
        sys.exit()
    if 0 == len(nginx_port):
        print('please input the nginx service port, default 8089')
        sys.exit()
    if 0 == len(mysql_port):
        print('please input the mysql service port, default 3306')
        sys.exit()
    if 0 == len(mysql_hostname):
        print('please input the nginx service hostname')
        sys.exit()
    if 0 == len(mysql_username):
        print('please input the nginx service username, default root')
        sys.exit()
    if 0 == len(mysql_password):
        print('please input the nginx service password')
        sys.exit()

    generate_config_file(loginserver_ip,loginserver_port,hydra_ip,hydra_port,login_consent_ip,login_consent_port,grafana_ip,grafana_port,nginx_ip,nginx_port,mysql_hostname,mysql_port,mysql_username,mysql_password)
    print('initial configurations success, configs could be found at loginserver_conf.ini/node_config.ini/hydra_config.ini/mysql_config.ini')
if __name__=="__main__":
    main(sys.argv[1:])