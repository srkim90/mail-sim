# -*- coding: utf-8 -*-

'''
  Author   : Kim, Seongrae
  Filename : sim_exit.py
  Release  : 1
  Date     : 2018-12-16
 
  Description : Mail simulator exit module
 
  Notes :
  ===================
  History
  ===================
  2018/12/16  created by Kim, Seongrae
'''
# common package import
from common import *   


def exit_handler():
    os.system('stty echo')
    sleep(0.01)
    quit()

