# -*- coding: utf-8 -*-

'''
  Author   : Kim, Seongrae
  Filename : main.py
  Release  : 1
  Date     : 2018-12-16
 
  Description : Mail simulator MMC function
 
  Notes :
  ===================
  History
  ===================
  2018/12/16  created by Kim, Seongrae
'''
# common package import
from common import *

# local package inport
from sim_exit import *
from signal_handler import *

class __mmc_quit(mmc):
    @staticmethod
    def run(command):
        exit_handler()


__mmc = [
    ["quit",                0, "quit"                                  , __mmc_quit                    ],
]

def mmc_run(index, name):
    mmc_parse.instance(__mmc, index, name)
    e = mmc_parse.getinstance()          

    try:
        e.run()                              
    except:
        print_call_stack()
        exit_handler()

    return
