# -*- coding: utf-8 -*-

'''
  Author   : Kim, Seongrae
  Filename : signal_handler.py
  Release  : 1
  Date     : 2018-12-16
 
  Description : Simulator signal handler module
 
  Notes :
  ===================
  History
  ===================
  2018/12/16  created by Kim, Seongrae
'''
# common package import
from common import *

from sim_exit import * 

class signal_handler(singleton_instance):
    signal_recv_time = 0
    def __init__(self):
        self.signal_init()

    def signal_init(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        hThread = threading.Thread(target=self.signal_wait)
        hThread.daemon = True
        hThread.start()

    def signal_wait(self):
        signal.pause()

    def signal_handler(self, signal, frame):

        if time.time() - self.signal_recv_time > 1:
            print("\n")
            PRINT('You pressed Ctrl+C!! If once again input within 1 sec, will quit.')
            self.signal_recv_time = time.time()
            return

        print("\n")
        exit_handler()

signal_handler.instance()
