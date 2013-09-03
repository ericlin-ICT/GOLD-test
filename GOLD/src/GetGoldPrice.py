'''
Created on 2013.7.31

@author: ericLin
'''

import urllib2
import time
from datetime import date
from time import strftime, localtime

import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

init_var_str = "1334.05DD19.909DD263.02DD3927DD1443.10DD732.28"

def getPrice(var_str):
  price_url = "http://js.xs9999.com/data/js/reflash_quote_page.php?var_str=" + var_str
  response = urllib2.urlopen(price_url)
  return response.read()

def parseResult(html):
  splited_html = html.split("var_str")
  var_str = splited_html[-1][2:-4]
  prices = var_str.split("DD")
  #print var_str
  price_dict = {"london_gold"   : prices[0],
                "london_silver" : prices[1],
                "rmb_gold"      : prices[2],
                "rmb_silver"    : prices[3],
                "platinum"      : prices[4],
                "palladium"     : prices[5]}
  #print price_dict 
  return price_dict,var_str

def toFile(price_dict):
  file_name = "../result/result-" + str(date.today()) + ".csv"
  res_file = open( file_name, 'a')
  line = strftime("%Y-%m-%d %H:%M:%S",localtime()) + ","\
         + price_dict["london_gold"]     + ","\
         + price_dict["london_silver"] + ","\
         + price_dict["rmb_gold"]      + ","\
         + price_dict["rmb_silver"]    + ","\
         + price_dict["platinum"]      + ","\
         + price_dict["palladium"]     + "\n"
  res_file.write(line)
  res_file.close( )

def run():
  var_str = init_var_str
  while(True):
    html = getPrice(var_str)
    price_dict,var_str = parseResult(html)
    toFile(price_dict)
    print var_str
    time.sleep(5)

def test():
  html = getPrice(init_var_str)
  print parseResult(html)
  
if __name__ == "__main__":
  #test()
  run()