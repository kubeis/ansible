# Zabbix 5.3+
## Installation
```shell
cd
wget https://repo.zabbix.com/zabbix/5.3/ubuntu/pool/main/z/zabbix-release/zabbix-release_5.3-1+ubuntu20.04_all.deb
sudo dpkg -i zabbix-release_5.3-1+ubuntu20.04_all.deb
sudo apt update
sudo apt install zabbix-server-pgsql zabbix-frontend-php php7.4-pgsql zabbix-apache-conf zabbix-sql-scripts zabbix-agent
# Installation de postgresql
docker run -d --name db -e POSTGRES_PASSWORD=password  -v /opt/postgres:/var/lib/postgresql/data \
  -p 5432:5432  systemdevformations/docker-postgres12  
  
```
## Creation de la base de donnees
```shell
# Connection a la base postgres
CREATE DATABASE zabbix;
CREATE ROLE zabbix WITH LOGIN ENCRYPTED PASSWORD 'zabbix';
```
## Population de la base de donnees
```shell
cd /usr/share/doc/zabbix-sql-scripts/postgresql
sudo -s
docker cp create.sql.gz db:/tmp/create.sql.gz
# dans le container db avec portainer
adduser zabbix 
cd /tmp
su - zabbix 
zcat create.sql.gz | psql zabbix
```
## Installer le GUI PHP
Completer l'installation 

## Mettre au point le zabbix-server 



