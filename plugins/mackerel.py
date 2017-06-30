# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from tools.mc_ctl import MackerelApi
from tools.tools import Tools
import re
import os

##  mackerel var ###

api_key=os.getenv("MACKEREL_APIKEY")

## servers

@respond_to('foo')
def hoge(message):
    message.reply('foobar')

@respond_to('^ping (.*)')
def ping_status(message, host):
    input_str = '{}'.format(host)
    if input_str is not None:
        target = Tools()
        nw_status = target.exec_ping(str(input_str))
        message.reply('{host} {reco}'.format(host=input_str, reco=nw_status))
    else:
        message.reply('Please set target!')

@respond_to('^cmd?')
def help_cmd(message):
    target = Tools()	
    yaml_file = target.get_yaml("/root/slackbot/plugins/tools/help.yml") 
    for k, v in yaml_file.items():
        message.reply('> {key} => {value}'.format(key=k,value=v))

@respond_to('^mc start (.*)')
def mackerel_agent_stop(message, host):
    input_str = '{}'.format(host)
    if input_str:	
	message.reply('mackerel agent start {}'.format(input_str))
    else:     
        message.reply('Please set target!') 

@respond_to('^mc stop (.*)')
def mackerel_agent_stop(message, host):
    message.reply('mackerel agent stop {}'.format(host))

@respond_to('^mc alert$')
def mackerel_agent_status(message):
    target = MackerelApi()
    alert_list = target.get_mc_alert(api_key)
    if alert_list is not None:
        for k, v in alert_list.items():
            message.reply('> {key}   => {value}'.format(key=k,value=v))
    else:
        pass

@respond_to('^mc alert close (.*) (.*)')
def mackerel_alert_close(message, alert_id=None, close_reason=None):
    target_id = '{}'.format(alert_id)
    close = '{}'.format(close_reason)
    target = MackerelApi()
    alert_status = target.get_value(str(target_id))
    if (alert_status is not None) and (close is not None):
        target.alert_close(target_id, str(close), api_key)
        message.reply(('> {} => is close!').format(str(target_id)))
    else:
        message.reply('> This alert is nothing!')

@respond_to('^mc status (.*)')
def mackerel_agent_status(message, host): 	
    input_str = '{}'.format(host)
    target = MackerelApi()
    if str(input_str) == "all":
        status_list = target.get_mc_status("all", api_key)
        for k, v in status_list.items():
            message.reply('> {key}   =>  {value}'.format(key=k,value=v))
    elif (str(input_str) is not None) and (target.get_value(str(input_str)) is not None):
	host_id = target.get_value(str(input_str)) 
        status_list = target.get_mc_status(str(host_id), api_key)
	message.reply('> {}'.format(status_list))	
    else: 
        message.reply('> Please set correct target!')

@respond_to('^mc (.*) (.*)')
def mackerel_agent_change(message, condition=None, host=None):
    input_str = '{}'.format(host) 
    target = MackerelApi()
    if (str(condition) is not None) and (re.match("working|wo", str(condition))):
        if target.get_value(str(input_str)) is not None:	
	    host_id = target.get_value(str(input_str))
	    target.change_mc_status(str(host_id), "working", api_key)
            message.reply(('> {} => working!').format(str(input_str)))
        else: 
            message.reply('> Please set correct target!') 
    elif (str(condition) is not None) and (re.match("poweroff|po", str(condition))): 
        if target.get_value(str(input_str)) is not None:
	   host_id = target.get_value(str(input_str))
	   target.change_mc_status(str(host_id), "poweroff", api_key)
           message.reply(('> {} => power off!').format(str(input_str))) 
        else:
	   message.reply('> Please set correct target!')	
    elif (str(condition) is not None) and (re.match("maintenance|ma", str(condition))):
        if target.get_value(str(input_str)) is not None: 
	   host_id = target.get_value(str(input_str))
	   target.change_mc_status(str(host_id), "maintenance", api_key)
           message.reply(('> {} => maintenance!').format(str(input_str)))
        else:
           message.reply('> Please set correct target!')
    elif (str(condition) is not None) and (re.match("standby|stb", str(condition))):
	if target.get_value(str(input_str)) is not None: 
           host_id = target.get_value(str(input_str))
	   target.change_mc_status(str(host_id), "standby", api_key)
           message.reply(('> {} => standby!').format(str(input_str)))
        else: 
           message.reply('> Please set correct target!') 
    elif (re.match("status", str(condition))):
        pass
    elif (re.match("alert", str(condition))):
        pass
    else:
        message.reply('> Please set correct option!')


