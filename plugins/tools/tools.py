#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from random import randint
import subprocess

###  define func ###

class Tools():

    def get_yaml(self, data):
	"""
        return yaml file value
	"""
        f = open(data, "r+")
        data = yaml.load(f)
        return data

    def random_digits(self, n):
	"""
	return random dint
	"""
	range_start = 10**(n-1)
	range_end = (10**n)-1
	return randint(range_start, range_end)

    def exec_ping(self, *args):
        """
        return dic status
        """
        status_dic = {}
        for x in list(args):
            try:
                subprocess.check_output(["ping", "-c", "2" , x ], stderr=subprocess.STDOUT)
                status_dic[x] = "OK"
            except subprocess.CalledProcessError as e:
                #print "returncode: {}".format(err.returncode)
                status_dic[x] = "NG"
        return status_dic

#if __name__ == '__main__':

