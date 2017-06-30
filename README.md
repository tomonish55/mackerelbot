**Git**   
https://github.com/lins05/slackbot

**How to start?**

    init.d/slackbot start / status / stop
    
**requirements module**

server install by pip

    pip install slackbot
    pip install pyyaml
    pip install requests
    pip install backports.ssl-match-hostname

**deployment**

default user home directory

**How to start slackbot?**

redis install and setup

    yum --enablerepo=epel install redis
    /etc/init.d/redis start
    chkconfig redis on

python setting

    python version 2.7.8 over
     
create log directory

    mkdir $HOME/slackbot/logs

env setting

    export MACKEREL_APIKEY="xxxxxxxxxxxxxxxxxxxxxxxxxxx"
    export SLACK_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxx" 

first time execute python shell

    python /slackbot/plugins/tools/mc_ctl.py 

**slack command options** 

```shel
## comannd help
>cmd?

## mackerel target status 
>mc status target 
```
       
