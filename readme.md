## 部署步骤：

#### 克隆此代码：

```
git clone http://10.10.7.232:8080/git/herunkang/login-deploy.git
cd login-deploy
```

 #### 解压出loginserver：

```
./unpack.sh
```

#### 配置：

```
python init.py --loginserver_ip 10.10.26.22 --loginserver_port 8003 --hydra_ip 10.10.26.22 --hydra_port 4443 --login_consent_ip 10.10.26.22 --login_consent_port 3001 --grafana_ip 10.10.26.22 --grafana_port 3000
```

#### 执行第一次部署：

```
./first_deploy.sh
```


此处会启动所有与登录相关的服务，包括loginserver/login-consent/hydra

## 运维：
#### 关闭所有的服务

```
./stop.sh
```

#### 启动所有的服务：

```
./deploy.sh
```
