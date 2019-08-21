<<'COMMENT'
# 如果使用其他用户 使用这段代码 然后在loginserver中配置
DBUSER="loginuser"
DBPASSWD="haCK3435#@$$%#@"
echo "create user ${DBUSER}"
create_db_sql="grant all privileges on ${DBNAME}.* to ${DBUSER}@'%' identified by ${DBPASSWD}"
echo ${create_db_sql}  | ${MYSQL_CMD}             
if [ $? -ne 0 ]
then
 echo "create user ${DBNAME} failed ..."
 exit 1
fi

COMMENT


