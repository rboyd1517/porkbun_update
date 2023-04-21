#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

keys = dict(secretapikey=config['secretapikey'], apikey=config['apikey'])
domain = config['domain']
id = config['id']
name = config['name']

resp = urllib.request.urlopen('http://wtfismyip.com/text')
ip = resp.read().decode('utf-8').strip('\n')

resp = urllib.request.urlopen(f'https://porkbun.com/api/json/v3/dns/retrieve/{domain}/{id}',
                              json.dumps(keys).encode('utf-8'))
data = json.loads(resp.read().decode('utf-8'))

old_ip = data['records'][0]['content']
if old_ip != ip:
    print(f'Updating ip from {old_ip} to {ip}.')
    post = dict(**keys, type='A', content=ip, name=name)
    resp = urllib.request.urlopen(f'https://porkbun.com/api/json/v3/dns/edit/{domain}/{id}',
                                  json.dumps(post).encode('utf-8'))

