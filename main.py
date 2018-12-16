# -*- coding: utf-8 -*-

'''
  Author   : Kim, Seongrae
  Filename : main.py
  Release  : 1
  Date     : 2018-12-16
 
  Description : Mail simulator main function
 
  Notes :
  ===================
  History
  ===================
  2018/12/16  created by Kim, Seongrae
'''
# common package import
from common import *

# local package inport
from mmc import *

class main:
    def __init__(self):
        ''' 1. Init Parameters'''
        name  = get_param(("--name","-n"), "mSim")
        index = get_param(("--index","-i"), 0)
        config_path  = get_param(("--config","-c"), "./config.cfg")

        ''' 2. Init Log'''
        try:
            sa_initlog(name, index, is_visible_log = True)
        except:
            do_abort()
     
        ''' 3. Init Config'''
        try:
            self.cfg = cfg_data(config_path)
        except:
            do_abort()
     
        ''' 4. Init Config'''
        self.print_title()

        ''' 5. Run MMC'''
        mmc_run(index, name)
        
        return 0

    def print_title(self):
        os.system("clear")
        PRINT("%s" % (LINE80) )
        PRINT("  S T A R T Mail Simulator (Configuration file : '%s')" % (self.cfg.data_path) )
        PRINT("%s" % (LINE80) )
        self.cfg.print_data_dictionary(is_title=False)

if __name__ == "__main__":
    main()
