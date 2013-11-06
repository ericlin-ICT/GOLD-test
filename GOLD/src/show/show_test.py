
# -*- coding:cp936 -*- 


from pylab import * 
from matplotlib.dates import DateFormatter, WeekdayLocator, HourLocator, DayLocator, MONDAY 
from matplotlib.finance import quotes_historical_yahoo, candlestick, plot_day_summary, candlestick2 
from matplotlib.font_manager import FontProperties 

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc",size=18) 
# ������ʼ����ֹ���ں͹�Ʊ���� 
date1 = ( 2012, 12, 25 ) 
date2 = ( 2013, 6, 1 ) 
stock_num = '000002.sz' 
# �������ڸ�ʽ 
mondays = WeekdayLocator(MONDAY) 
alldays = DayLocator() 
weekFormatter = DateFormatter('%b %d') 
dayFormatter = DateFormatter('%d') 
# ��ȡ��Ʊ���� 
quotes = quotes_historical_yahoo(stock_num, date1, date2) 
if len(quotes) == 0: 
 raise SystemExit 

# ���������߻������� 
fig = figure() 
fig.subplots_adjust(bottom=0.2) 
ax = fig.add_subplot(111) 
ax.xaxis.set_major_locator(mondays) 
ax.xaxis.set_minor_locator(alldays) 
ax.xaxis.set_major_formatter(weekFormatter) 

#ע�͵����������һ�У����Եõ������߻������� 
candlestick(ax, quotes, width=0.6) 

#plot_day_summary(ax, quotes, ticksize=3) 
ax.xaxis_date() 
ax.autoscale_view() 
setp( gca().get_xticklabels(), rotation=45, horizontalalignment='right') 
title(u'ƽ������ 2012,12,25-2013,6,1',fontproperties=font) 
show()