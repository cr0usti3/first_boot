#!/usr/bin/env python
#-*- coding: utf8 -*-

from fabric.api import env, local, settings, abort, run, cd,put
import os.path
import yaml
import sys


try :
    with open('config.yaml','r') as conf :
        env.roledefs=yaml.load(conf)
except IOError :
    print ('Need a YAML config file')
    sys.exit()

env.user='root'


def memory():
    run('free -m ')

# determine os type
def osdef() :
    if os.path.isfile('/etc/debian_version') :
        return 'apt'
    elif os.path.isfile('/etc/redhat-release'):
        return 'yum'

def motd():

    if 'apt' in osdef() :
        with settings(warn_only=True):
            run('apt-get update')
            run('apt-get install -y  screenfetch')
            run('rm /etc/motd')
            run('ln -s /var/run/motd /etc/motd')
            run('mkdir /etc/update-motd.d')
            put('motd.d/10-system','/etc/update-motd.d')
            run('chmod +x /etc/update-motd.d/10-system')

def ntp():
    run('apt-get install -y  openntpd ')
    run('apt-get install -y  ntpdate')



