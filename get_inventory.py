#!/usr/bin/env python

#'''
#Example custom dynamic inventory script for Ansible, in Python.
#'''

import argparse
import sqlalchemy
from sqlalchemy import create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, Column, Integer, String
from sqlalchemy.orm import sessionmaker

try:
    import json
except ImportError:
    import simplejson as json

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    employeename = Column(String)
    deptid = Column(Integer, primary_key=True)
    employeesalary = Column(Integer)
    managerid = Column(Integer)

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    deptname = Column(String)

class Interface (Base):
    __tablename__ = 'interface'
    interfaceid = Column(Integer, primary_key=True)
    hostid = Column(Integer)
    main = Column(Integer)
    type = Column(Integer)
    useip = Column(Integer)
    ip = Column(String)
    dns = Column(String)
    port = Column(String)
    available = Column(Integer)
    error = Column(String)
    errors_from = Column(Integer)
    disable_until = Column(Integer)

class Hosts(Base):
    __tablename__ = 'hosts'
    hostid = Column(Integer,primary_key=True)
    proxy_hostid = Column(Integer)
    host = Column(String)
    status = Column(Integer)
    lastaccess = Column(Integer)
    ipmi_authtype = Column(Integer)
    ipmi_privilege = Column(Integer)
    ipmi_username = Column(String)
    ipmi_password = Column(String)
    maintenanceid = Column(Integer)
    maintenance_status = Column(Integer)
    maintenance_type = Column(Integer)
    maintenance_from = Column(Integer)
    name = Column(String)
    flags = Column(Integer)
    templateid = Column(Integer)
    description = Column(String)
    tls_connect = Column(Integer)
    tls_accept = Column(Integer)
    tls_issuer = Column(String)
    tls_subject = Column(String)
    tls_psk_identity = Column(String)
    tls_psk = Column(String)
    proxy_address = Column(String)
    auto_compress = Column(Integer)
    discover = Column(Integer)
    custom_interfaces = Column(Integer)
    uuid  = Column(String)

class Hosts_groups(Base):
        __tablename__ = 'hosts_groups'
        hostgroupid  = Column(Integer, primary_key=True )
        hostid  = Column(Integer)
        groupid = Column(Integer)


class ExampleInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.example_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory))

    # Example inventory for testing.
    def example_inventory(self):
        return {
            'group': {
                'hosts': ['172.17.0.4' ],
                'vars': {
                    'ansible_ssh_user': 'ubuntu',
                    'ansible_ssh_password': 'Passw0rd'
                }
            },
            '_meta': {
                'hostvars': {
                    '51.255.211.168': {
                        'host_specific_var': 'centos'
                    }
                }
            }
        }

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


# Get the inventory.
engine = create_engine ('postgresql+psycopg2://zabbix:zabbix@192.168.1.82/zabbix',echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
hrdept = Department(id=1, deptname='HR')
financedept = Department(id=2, deptname='Finance')
techdept = Department(id=3, deptname='Tech')
marketingdept = Department(id=4, deptname='Marketing')
session.add_all([hrdept, financedept, techdept, marketingdept])
session.commit()
session.add_all([Employee(id=1, employeename='Alex', deptid=1, employeesalary=60000, managerid=None),
                Employee(id=2, employeename='Martha', deptid=1, employeesalary=45000, managerid=1),
                Employee(id=3, employeename='Merlyn', deptid=1, employeesalary=46000, managerid=1),
                Employee(id=4, employeename='Daisy', deptid=2, employeesalary=66000, managerid=None),
                Employee(id=5, employeename='Mike', deptid=2, employeesalary=56000, managerid=4),
                Employee(id=6, employeename='Raj', deptid=2, employeesalary=54000, managerid=4),
                Employee(id=7, employeename='Marry', deptid=3, employeesalary=96000, managerid=None),
                Employee(id=8, employeename='Sam', deptid=3, employeesalary=76000, managerid=7)])
session.commit()
#print(session.query(func.count(Department.id)).scalar())
#print(session.query(func.count(Department.id)).all())

print(session.query(Interface.ip).join(Hosts, and_(Interface.hostid==Hosts.hostid,Hosts.status == 0)).
      join(Hosts_groups,and_(Hosts_groups.hostid==Hosts.hostid,Hosts_groups.groupid == 5)).all())


#select i.ip,h.name from hosts h, interface i, hosts_groups g
#where h.hostid = i.hostid and h.hostid = g.hostid and h.status=0 and g.groupid = 5;



ExampleInventory()
