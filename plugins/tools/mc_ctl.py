#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import json
import redis
import os

##  mackerel var ###

api_key=os.getenv("MACKEREL_APIKEY")

### prepare step ###

try:
    con = redis.StrictRedis(host='localhost', port=6379, db=0)
    con.set('test', 'hello')
except:
    print "Please start redis server!"
    sys.exit(2)

###  define func ###

class MackerelApi():

    def get_mc_id(self, apikey):
	"""
        return mackerel host id list 
	"""
        headers = {'X-Api-Key': apikey}
	r = requests.get('https://mackerel.io/api/v0/hosts', headers=headers)
        j_values = r.json()
        host_list = j_values["hosts"]
        host_id_list = []      
	for x in  list(host_list):
	    host_id_list.append(str(x["id"]))
        return host_id_list 

    def get_mc_hostname(self, lt_mc_id, apikey):
	"""
	first arg specific mackerel id
	return mackerel host name list
	"""
	hos_name_list = []    
        for x in list(lt_mc_id):
	    headers = {'X-Api-Key': apikey}
	    r = requests.get(('https://mackerel.io/api/v0/hosts/%s' % x ), headers=headers)
            j_values = r.json()
	    host_info = j_values["host"]
            hos_name_list.append(str(host_info["name"]).rstrip(".co.jp"))
        return hos_name_list 

    def get_mc_alert(self, apikey):
        """
        get alert and set alert
        """
        headers = {'X-Api-Key': apikey}
        r = requests.get('https://mackerel.io/api/v0/alerts', headers=headers)
        j_values = r.json()
        alert_list = j_values["alerts"]
        alert_dic = {}
        for x in alert_list:
            alert_dic[str(x['id'])] = str(x['status'])
            self.set_value(str(x['id']), str(x['status']))
        return alert_dic

    def alert_close(self, alert_id, text, apikey):
        """
        mackerel alert close
        first arg alert id
        second arg close reason
        """
        ### all change param ###
        current_alert = self.get_value(str(alert_id))
        if current_alert is not None:
            payload = {'reason': str(text)}
            headers = {'X-Api-Key': apikey, 'content-type': 'application/json'}
            url = ('https://mackerel.io/api/v0/alerts/%s/close' % alert_id )
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            self.del_value(str(alert_id))
        else:
           return current_alert

    def get_mc_status(self, mc_id, apikey):
	"""    
	first arg specific mackerel id
        return mackerel host status
        """
        ### all status get param ###
	if str(mc_id) == "all":   
            host_status = {} 		
	    for x in self.get_mc_id(apikey):	
	        headers = {'X-Api-Key': apikey}
		r = requests.get(('https://mackerel.io/api/v0/hosts/%s' % x ), headers=headers)
		j_values = r.json()
		host_info = j_values["host"]
                lc_value = host_info["status"]
                lc_key = self.get_value(str(x))          
                host_status[lc_key] = lc_value
            return host_status 
        else: 
            headers = {'X-Api-Key': apikey}
	    r = requests.get(('https://mackerel.io/api/v0/hosts/%s' % mc_id ), headers=headers)
            j_values = r.json()
            host_info = j_values["host"]
            return host_info["status"] 

    def change_mc_status(self, mc_id, mc_status, apikey):
        """
	mackerel status change 
	first arg specific mackerel id
        second arg status  standby, working, maintenance, poweroff
        """  
	### all change param ###
	if str(mc_id) == "all":		
            mackerel_id = self.get_mc_id(apikey)
	    for x in mackerel_id:
                payload = {'status': mc_status}
                headers = {'X-Api-Key': apikey, 'content-type': 'application/json'}
		url = ('https://mackerel.io/api/v0/hosts/%s/status' % x ) 
		r = requests.post(url, data=json.dumps(payload), headers=headers)
        else:
            payload = {'status': mc_status}
	    headers = {'X-Api-Key': apikey, 'content-type': 'application/json'}
	    url = ('https://mackerel.io/api/v0/hosts/%s/status' % mc_id )
	    r = requests.post(url, data=json.dumps(payload), headers=headers)

    def register_host_info(self, lt_mc_id, lt_host_name): 
        """
        register mackerel  { key  hostname : value mackerel_id }
	first arg  mackerel_id list, second arg hostname list   
	"""
        merge_list = zip(lt_host_name, lt_mc_id)
	for x, y  in  merge_list:
	    self.set_value(str(x), str(y))	
	    self.set_value(str(y), str(x))	
        ### all mackerel all id and host name set ###
        self.set_value("mc_id_all", tuple(lt_mc_id)) 
	self.set_value("mc_name_all", tuple(lt_host_name))

    def set_value(self, key, value):
        """
	redies value set
	""" 
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	r.set(key, value) 

    def get_value(self, key):
        """
	redies value get
	"""
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
        values = r.get(key)
	return values

    def del_value(self, key):
        """
        redies delete key
        """
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        current_key = self.get_value(key)
        if current_key is not None:
            r.delete(key)
        else:
            return "None"

if __name__ == '__main__':

    a = MackerelApi()
    b = a.get_mc_id(api_key)
    c = a.get_mc_hostname(b, api_key)
    z = a.register_host_info(b, c)
