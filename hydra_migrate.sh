# install postgre
# apt-get install postgresql -y

# create database
# using mysql container

# add system user
#useradd hydra
#passwd hydra

# migrate
./hydra migrate sql postgres://hydra:secret@localhost:5432/hydra?sslmode=disable

