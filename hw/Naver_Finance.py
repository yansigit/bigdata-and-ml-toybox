import pandas as pd
import requests
from bs4 import BeautifulSoup

res = requests.get('https://finance.naver.com/sise/sise_quant.nhn')

bs = BeautifulSoup(res.text, 'html.parser')
res = bs.find('div', class_='box_type_l')

df = pd.read_html(str(res))[0]

companies = list(df['종목명'].dropna())
print('현재 네이버 금융 국내 코스피 상위 100 기업 목록')
print(companies)
ret = dict(zip(companies, list(df['현재가'].dropna().astype(int))))

print('현재 주가는', ret[input('주가 검색할 기업이름: ')], '원 입니다')
