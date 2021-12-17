# 파이썬으로 네이버 금융 크롤링

파이썬 자체에 FinanceDataReader나 pykrx와 같이 주가 데이터를 제공하는 패키지가 존재한다.

하지만, ETF의 종목별 외인, 기관 수급은 파악할 수 없고, 주가, 기관 수급, 당일 거래량 등이 따로따로 되어있어 하나로 merging하는데 귀찮음이 있다.

그래서 간단한 분석이 필요할때는 네이버 금융에 있는 데이터를 크롤링하는게 빠르다.

____

크롤링할 데이터는 네이버금융에 종목별 투자자별 매매도향에 있는 외국인 기관 순매매 거래량 테이블이다.

해당 테이블에서 날짜, 종가, 거래량, 기관 순매매량, 외국인 순매매량, 외국인 보유주수, 외국인 보유율을 크롤링하는 함수를 만들고 종목별, 페이지수를 설정하여 데이터프레임을 완성시킬 수 있게 하였다.



<img width="696" alt="스크린샷 2021-12-17 오후 3 13 40" src="https://user-images.githubusercontent.com/73429381/146498725-488a4afc-4a6e-4045-b94b-8c1c00b2264e.png">



_____



```python
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
        p = parser.make2d(table_html[2]) #html을 2차원 테이블 형태로 변황
        table = pd.DataFrame(p,columns=p[0]).iloc[:,[0,1,4,5,6,7,8]] #원하는 컬럼만 추출
        table = table.drop([0,1,2,8,9,10,16,17,18,24,25,26,32]) # 빈 행 제거
        all_table = pd.concat([all_table,table],axis=0)
    
    all_table.columns = ['날짜','종가','거래량','기관','외국인','외인보유수','외인보유율']
    all_table = all_table.set_index('날짜')
    
    #데이터 전처리
    for i in all_table.columns.values:
        all_table[i] = all_table[i].str.replace(',','')
        all_table[i] = all_table[i].str.replace('%','')
    
    all_table = all_table.astype(float)
    all_table['외인보유율'] = all_table['외인보유율']/100
    
    return all_table
  
  df = get_table_html('000660',16)
  df.head()

```

| 날짜       | 종가   | 거래량  | 기관    | 외국인  | 외인보유수 | 외인보유율 |
| ---------- | ------ | ------- | ------- | ------- | ---------- | ---------- |
| 2021.12.16 | 124000 | 3869086 | -135694 | 472815  | 355173546  | 0.4879     |
| 2021.12.15 | 123500 | 2681332 | 122649  | 569789  | 354813704  | 0.4874     |
| 2021.12.14 | 121000 | 2201003 | -143587 | 90162   | 354310621  | 0.4867     |
| 2021.12.13 | 121500 | 3329176 | 237667  | 545870  | 354264832  | 0.4866     |
| 2021.12.10 | 120500 | 2512642 | -388148 | -290101 | 353694134  | 0.4858     |
| 2021.12.09 | 123500 | 5631833 | 384865  | 829870  | 355030959  | 0.4877     |
| 2021.12.08 | 120000 | 6168137 | 330002  | -426686 | 354171600  | 0.4865     |
| 2021.12.07 | 121500 | 5112025 | 519010  | 839374  | 354398286  | 0.4868     |
| 2021.12.06 | 118500 | 4318893 | 195101  | 51774   | 353561466  | 0.4857     |
| 2021.12.03 | 118000 | 4567843 | 10691   | -341639 | 353274692  | 0.4853     |
| 2021.12.02 | 120000 | 6980518 | 426484  | 910664  | 353549239  | 0.4856     |
