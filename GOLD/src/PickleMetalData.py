#-*- encoding: utf-8 -*-
'''
Created on 2013年10月30日

@author: ericlin
'''

import pickle

class PickleData(object):
  '''
  pickle data interface
  '''
  def dump(self, filename):
    pickle.dump(self, file=filename, protocol=None)
  
  def load(self, filename):
    return pickle.load(file=filename)



class PickleMetalData(PickleData):
  '''
    Metal Data Obj
  '''

  def __init__(self, sr_num, dt_time, df_realtime_pri ):
    '''
    Constructor
    '''
    self.low_pri     = sr_num['low_pri']
    self.high_pri    = sr_num['hig_pri']
    self.lastclo_pri = sr_num['lastclo_quo']
    self.open_pri    = sr_num['ope_quo']
    self.price_chg   = sr_num['price_chg']
    self.curr_pri    = sr_num['curr_cod']
    self.new_pri     = sr_num['new_pri']
    
    self.dt_time = dt_time
    
    self.df_realtime_pri = df_realtime_pri
  
  def dump(self, filename):
    PickleData.dump(self, filename)
  
  def load(self, filename):
    return PickleData.load(self, filename)
        