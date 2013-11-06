#-*- encoding: utf-8 -*-
'''
Created on 2013年10月11日

@author: ericlin
'''

import urllib2

import logging
import json
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import pickle
from numpy.core._mx_datetime_parser import datetime_from_string
from PickleMetalData import PickleMetalData

logging.basicConfig(level=logging.DEBUG,
              format='%(levelname)s %(message)s')

class CCBPreciousMetal(object):
  '''
  CCB precious metal 
  '''
  
  RMB_Silver_no = '020001'
  RMB_Pt_no     = '030001'
  RMB_AU9999_no = '019999'
  RMB_AU9995_no = '019995'
  day_prefix      = "http://tool.ccb.com/waihui/trendchart/day/" # 日线前缀
  week_prefix     = "http://tool.ccb.com/waihui/trendchart/week/"# 周线前缀
  month_prefix    = "http://tool.ccb.com/waihui/trendchart/month/" # 月线前缀 
  realtime_prefix = "http://tool.ccb.com/webtran/static/trendchart/getAccountData.gsp?dateType=timeSharing&sec_code="
  
  def __init__(self):
    self.pickle_data = None

  def process_realtime(self, price_data):
    #print price_data
    #print price_data.keys()
    pass
  
    
  def getPriceData(self, no=RMB_AU9999_no, data_type=realtime_prefix):
    '''
    Description:
      get precious metal price data
      
    Args:
      no        precious metal number including RMB_Silver_no,RMB_AU9995_no,RMB_AU9999_no,RMB_Pt_no
                (default RMB_AU9999_no)
      data_type  the kind of data, including day, week, month and realtime
                (default real_time)
    Return:
      dict obj with price data 
    '''
    http_url = data_type + str(no) # 拼凑数据url
    response = self.__getHttpRes(http_url)
    return self.__getJson(response)


  def load(self, filename):
    '''
    '''
    return pickle.load(filename)
  
  def dump(self, data, filename):
    '''
    '''
    if self.pickle_data is not None:
      self.pickle_data.dump(filename)
  
  def parse(self, rt_data):
    '''
    '''
    try:
      # 取得数值项
      low_pri     = float(rt_data[u'low_pri'])
      high_pri    = float(rt_data[u'hig_pri'])
      lastclo_pri = float(rt_data[u'lastclo_quo'])
      open_pri    = float(rt_data[u'ope_quo'])
      price_chg   = float(rt_data[u'price_chg'])
      curr_pri    = float(rt_data[u'curr_cod'])
      new_pri     = float(rt_data[u'new_pri'])
      index = ['low_pri', 'hig_pri', 'lastclo_quo', 'ope_quo', 'price_chg', 'curr_cod', 'new_pri']
      num   = [low_pri, high_pri, lastclo_pri, open_pri,price_chg, curr_pri, new_pri]
      sr_num = Series(num, index = index)
      
      # 取得时间
      time = rt_data[u'time']
      dt_time = datetime_from_string(time)
      logging.debug(type(dt_time))
      
      # 实时数据
      realtime_pri = rt_data[u'realTimePrice']
      lst_realtime_pri = json.loads(realtime_pri)
      columns = ['CURR_COD', 'new_pri', 'price_chg', 'time', 'valueB', 'valueS']
      df_realtime_pri = DataFrame(lst_realtime_pri, columns=columns)
      logging.debug(df_realtime_pri)
      logging.debug(type(df_realtime_pri['time']))
      dt_array = list()
      for item in df_realtime_pri['time']:
        dt = datetime_from_string(item)
        dt_array.append(dt)
      df_realtime_pri['time'] = dt_array
      
      self.pickle_data = PickleMetalData(sr_num, dt_time, df_realtime_pri)
      return self.pickle_data
    
    except KeyError, e:
      logging.info("KeyError! " + e)
      return None
    #except e:
    #  logging.exception("exception! " + e)
    #  return None
    
    
  def compute(self, data):
    '''
    '''
    df_realtime_pri = data.df_realtime_pri
    df_realtime_pri['new_pri'].plot()
    plt.show()
    pass
    
  def __getHttpRes(self, url):
    '''
    Description:
      send http request, get the response object
    Args:
      url  price url address
    Return:
      urllib2 response object
    '''
    return urllib2.urlopen(url)
  
  def __getJson(self, response):
    '''
    Description:
      get list from josn format response
    Args:
      response  urllib2 response object
    Return:
      list object
    '''
    res = json.load(response)
    #logging.debug("json dict %s", res)
    return res
    
 

    

if __name__=="__main__":
  a = CCBPreciousMetal()
  price = a.getPriceData()
  a.process_realtime(price)
  data = a.parse(price)
  a.compute(data)
