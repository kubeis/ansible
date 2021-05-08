# Installation du bac a sable ansible

Connectez-vous a la VM fournie lors du debut du cours

## Pre-requis pour ubuntu 20.04
```shell
sudo apt update   # update all packages
sudo apt -y install sshpass # allow using ssh with a password
sudo apt -y install python3-venv
#fork and clone ---> git clone https//github.com/kubeis/ansible
cd ansible 
python3 -m venv venv # set up the module venv in the directory venv
source venv/bin/activate # activate the python virtualenv
pip3 install wheel # set for permissions purpose
pip3 install ansible # install ansible
pip3 install requests # extra packages 
ansible --version  # check version number , should be the latest 2.10.9+
ansible-playbook -i inventory install_docker_ubuntu.yml --limit local # run a playbook
su - $USER
cd ansible
source venv/bin/activate # activate the python virtualenv
```

## Installation de portainer pour verifier les resultats de nos tps 
```shell
docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer -H unix:///var/run/docker.sock 
```

## Mise en place des containers   
Demarrez ces 3 containers pour simuler differentes machines.    
```shell script
docker run -d --name target1 systemdevformations/ubuntu_ssh:v2  
docker run -d --name target2 systemdevformations/centos_ssh:v5 
docker run -d --name target3 --env ROOT_PASSWORD=Passw0rd systemdevformations/alpine-ssh:v1   
```
Checkez si les containers sont presents  
Faire un ```docker ps | grep systemdevformation``` 

```shell script
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS                    PORTS                  NAMES
f5034036dc56        systemdevformations/alpine-ssh:v1   "/entrypoint.sh"         11 hours ago        Up 11 hours               22/tcp                 target3
c714f0b92509        systemdevformations/centos_ssh:v5   "/usr/bin/supervisor…"   23 hours ago        Up 23 hours (unhealthy)   22/tcp                 target2
6051c68c1712        systemdevformations/ubuntu_ssh:v2   "/usr/sbin/sshd -D"      23 hours ago        Up 23 hours               22/tcp                 target1              target1  
```  

## Copiez votre fichier inventory_template dans inventory  
Changez le fichier inventory avec les nouvelles adresses IP des containers et de votre vm remote 
et retrouver les adresses IP des containers target1, target2 et target3, et notez les 
 ```shell script
docker network inspect bridge
```
en fonction de l'adresses IP de la VM remote fournie pendant le cours     
modifier egalement cette adresse ip     

Dans votre home directory,  faire  
```ssh-keygen -t rsa -b 4096 ```  
Valider les parametres par defaut en tapant enter a chaque etape 
sans passphrase   
```ssh-copy-id centos@<remote_id_address>```

## Commandes Ad-Hoc
Faire la commande Ansible Ad-Hoc ci-dessous pour verifier si votre fichier inventory est correct.
```ansible all -m ping -i inventory```
Faire ensuite  les Ad-Hoc commandes suivantes l'une apres l'autre, lentement:  
```shell script 
ansible centos -m yum -a "name=elinks state=latest" -i inventory
ansible ubuntuvm -m apt -a "name=elinks state=latest" -i inventory
ansible ubuntuvm -b -m apt -a "name=elinks state=latest" -i inventory
ansible all --list-hosts -i inventory
ansible all -m setup -a "filter=ansible_default_ipv4"  -i inventory
ansible all -m setup -a "filter=ansible_distribution"  -i inventory 
ansible all -m setup -a "filter=ansible_distribution_version"  -i inventory 
ansible all -m command -a "df -h" -i inventory
NE PAS FAIRE LA COMMANDE SUIVANTE ELLE PREND 10 MINUTES
# -- ansible centos -b -m yum -a "name=* state=latest" -f 10  -i inventory  # default = 5
ansible centos -m file -a "dest=/home/centos/testfile state=touch" -i inventory 
```
## Groupes de hosts
Mettre a jour les adresses IP dans le fichier inventory_children sans en modifier 
la structure.  

## Premier script YAML
Dans la directory ansible-examples editez le fichier ansible_ping.yml, et etudiez le code. 
## Premieres commandes ansible-playbook
 ```shell script
ansible-playbook  -i inventory_children ansible_ping.yml  --limit ubuntu
ansible-playbook  -i inventory_children ansible_ping.yml  --limit centos
````
## Ad-Hoc commande pour afficher les facts 
```ansible target2 -i inventory_children -m setup```

## Les facts dans un fichier YAML
### Utilisation de when 
```ansible-playbook -i inventory_children ansible_facts_using_when.yml```
### Utilisation de la commande assert 
```ansible-playbook -i inventory_children ansible_facts_using_assert.yml```  

### Le prompt et les conditions
```ansible-playbook -i inventory_children conditions.yml --limit centos```

### les boucles
```ansible-playbook -i inventory_children loops.yml --limit centos```

## Passage d'information entre les hosts
### In-memory inventory  
Pour passer des variables entre remote-to-remote host il est possible
de creer un host de type dummy et lui attacher des variables pour les passer 
vers l'autre host.

```ansible-playbook -i inventory_children runtime_inventory_additions.yml```

### Deploiement d'une cle ssh vers des slave hosts

```shell script
 ansible-playbook -i inventory_children propagate_ssh_key.yml 
```

### Inventaire dynamique
Mise en place d'une application-tier dans laquelle les devices a maintenir avec 
ansible sont mis a jour. 
#### Exemple avec l'applicationde monitoring Zabbix

```shell
docker run -d --name db -e POSTGRES_PASSWORD=password  -v /opt/postgres:/var/lib/postgresql/data \
  -p 5432:5432  systemdevformations/docker-postgres12
wget https://repo.zabbix.com/zabbix/5.3/ubuntu/pool/main/z/zabbix-release/zabbix-release_5.3-1+ubuntu20.04_all.deb
sudo dpkg -i zabbix-release_5.3-1+ubuntu20.04_all.deb
sudo apt update
sudo apt install -y zabbix-server-pgsql zabbix-frontend-php php7.4-pgsql zabbix-apache-conf zabbix-sql-scripts zabbix-agent
```


Faire un fork de ce repo  
```https://github.com/crunchy-devops/ansible-dynamic-inventory.git```
dans votre repo github personnel
et faire un git clone, dans votre home directory, et dans la vm ansible controller   
Changer le fichier get_inventory.py   
mettre l'adresse IP de votre remote VM dans la structure JSON 
```shell script
'group': {
          'hosts': ['51.68.28.179' ],
```
Save, git commit and git push
et  tapez dans votre VM
```ansible-playbook -i get_inventory.py playbook.yml```


## Utilisation des variables et des filtres 
Retourner dans ansible-examples
### Changer the Message Of The Day (MOTD) 
```ansible-playbook -i inventory_children motd.yml```

### Les filters, creer son propre filtre 
```ansible-playbook -i inventory_children new_filter.yml --limit target2```

## Les modules
### Creer son propre module 
Allez dans votre compte github pour creer un token   
cliker sur les Settings de votre compte github et selectionnez  
Developer Settings et ensuite Personnal Access Tokens 
Creer un token et lui donner les droits pour creer un repo github.  
Dans votre home directory faire un ```vi token``` et copier votre
token.  
Toujours sous le prompt venv dans votre directory ansible-examples
faire ```pip3 install requests``` et 
```ansible-playbook -i inventory_children ansible_create_module.yml```

## Les Roles
### Mettre le precedement playbook dans un role 
Dans votre home directory toujours sous le prompt venv
faire ```mkdir example-role```  
et ```cd example-role```  
```ansible-galaxy init github.role```  
creer un ficher playbook.yml    
```yaml
---
- name: use a dedicated Ansible module
  hosts: localhost
  roles:
    - { role: github.role }
```
Dans example-role/github.role/tasks/main.yml 
copier le code suivant
```yaml
# tasks file for github.role
- name: Create a github Repo
  github_repo:
    github_auth_key: "{{ git_key }}"
    name: "repo-create-with-ansible"
    description: "Ansible module for github"
    private: no
    has_issues: no
    has_wiki: no
    has_downloads: no
    state: present
  register: result
```
Dans  example-role/github.role/defaults/main.yml
```yaml
# defaults file for github.role
git_key: d6f90b4be8axxxxxxxxxxxxxxx
```
Dans votre directory example-role, faire un 
```shell script
   cp -r ../ansible-examples/library . 
   cp -r ../ansible-examples/inventory_children . 
```
Tapez la commande suivante: 
```ansible-playbook -i inventory_children playbook.yml```

## Ansible Vault
Nous allons voir comment crypter nos informations sensibles avec Ansible
Crypter la variable token dans votre projet example defaults/main.yml  
Tapez  
```ansible-vault encrypt  main.yml```   
entrez votre mot de passe   
mettrez ce mot de passe dans un fichier  
```vi /home/<home_directory>/mysecret```   
Vous pouvez executer le playbook avec dans example-role directory   
```ansible-playbook -i inventory_children --vault-password-file /home/<home_directory>/mysecret playbook.yml``` 
vous pouvez metter le path de ce fichier dans votre ```.bash_profile``` file.  
```export  ANSIBLE_VAULT_PASSWORD_FILE=/home/<home>/mysecret```      
et vous entrez la commande sans vous soucier du fichier du mot de passe  
```ansible-playbook -i ../inventory_children playbook.yml``` 









