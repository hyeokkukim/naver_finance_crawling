import pandas as pd
import numpy as np

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
from html_table_parser import parser_functions as parser

def get_table_html(ticker,page):
    base_url = 'https://finance.naver.com/item/frgn.nhn?code='+str(ticker)+'&page={}'
    all_table = pd.DataFrame()
    for n in range(page):
        url = base_url.format(n+1)
        req = urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        table_html = soup.find_all('table')
        p = parser.make2d(table_html[2])
        table = pd.DataFrame(p,columns=p[0]).iloc[:,[0,1,4,5,6,7,8]]
        table = table.drop([0,1,2,8,9,10,16,17,18,24,25,26,32])
        all_table = pd.concat([all_table,table],axis=0)
    
    all_table.columns = ['날짜','종가','거래량','기관','외국인','외인보유수','외인보유율']
    all_table = all_table.set_index('날짜')

    for i in all_table.columns.values:
        all_table[i] = all_table[i].str.replace(',','')
        all_table[i] = all_table[i].str.replace('%','')
    all_table = all_table.astype(float)
    all_table['외인보유율'] = all_table['외인보유율']/100
    
    return all_table



df = get_table_html('000660',16)
df.to_excel('df.xlsx')


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(name='2019', x=ppl['행정동명'], y=ppl['2019'], marker_color = '#173f5f'),secondary_y= False)
fig.add_trace(go.Bar(name='2020', x=ppl['행정동명'], y=ppl['2020'], marker_color = '#3ca2a3'),secondary_y= False)
fig.add_trace(go.Bar(name='2021', x=ppl['행정동명'], y=ppl['2021'], marker_color = '#f6d55c'),secondary_y= False)


fig.add_trace(
    go.Scatter(name = '2019/2020', x = ppl['행정동명'], y = ppl['2019/2020'],mode = 'lines + markers',marker_color = '#20639b'),
    secondary_y=True)
fig.add_trace(
    go.Scatter(name = '2019/2021', x = ppl['행정동명'], y = ppl['2019/2021'],mode = 'lines + markers',marker_color = '#ed553b'),
    secondary_y=True)

fig.update_yaxes(title_text="연도별 생활인구 변동추이", secondary_y=False)
fig.update_yaxes(title_text="2019년 대비 생활인구 변동추이", secondary_y=True)
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
fig.show()