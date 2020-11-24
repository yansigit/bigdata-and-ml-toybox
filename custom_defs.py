import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_newspapers():
    url = "https://news.naver.com/main/officeList.nhn"
    # 크롤링 차단하고 있으므로 User-Agent 지정하여 우회
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(html.text, 'html.parser')

    # 신문 제공사 딕셔너리
    # 신문사이름: 신문사번호
    newspapers = {}

    # css selector 이용하여 파싱
    for ele in soup.select('ul.group_list a'):
        newspapers[ele.text] = (ele['href'].split('&oid=')[1])

    # 파라미터 붙어서 수동할당
    newspapers['연합뉴스'] = '001'

    return newspapers


def start_parse(company):
    # 정치, 경제, 사회, 생활/문화, 세계, IT/과학, 오피니언 중 선택
    # subject = '정치'

    daterange = pd.date_range(start='20201001', end='20201031').strftime('%Y%m%d')
    datarange = [str(date) for date in daterange]

    # 분류 딕셔너리
    sids = {'정치': '100', '경제': '101'}  # '사회': '102', '생활/문화': '103', '세계': '104', 'IT/과학': '105', '오피니언': '110'}

    # 신문사 넘버
    newspapers = get_newspapers()
    company_num = newspapers[company]

    # 분야 번호
    # sid = sids[subject]

    # dataFrame dictionary
    # news = {'신문사': [], '제목': [], 'link': []}

    result_list = {'정치': set(), '경제': set()}

    for date in daterange:
        for sid in sids:
            # 뉴스 페이지들 끝 번호 알아내기
            url = "https://news.naver.com/main/list.nhn?mode=LPOD&listType=title&sid1={}&mid=sec&oid={}&date={}&page=9999".format(
                sids[sid], company_num, date)
            html = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'})
            soup = BeautifulSoup(html.text, 'html.parser')
            pages = soup.select('div.paging strong')

            if len(pages) > 0:
                lastpage = int(pages[-1].text)

            # 각 페이지마다
            for page in range(lastpage):
                list_url = "https://news.naver.com/main/list.nhn?mode=LPOD&listType=title&sid1={}&mid=sec&oid={}&date={}&page={}".format(
                    sids[sid], company_num, date, page)
                list_html = requests.get(list_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'})
                list_soup = BeautifulSoup(list_html.text, 'html.parser')

                # print(list_url)

                # 뉴스 인덱스
                elem_index = 0
                # 각 뉴스 기사마다
                for element in list_soup.select('div.list_body ul a'):

                    if element.find('img') is not None:
                        continue

                    try:
                        article_date = list_soup.select('span.date')[elem_index].text
                        article_date = article_date.split('. ')[0]
                        article_date = datetime.strptime(article_date, '%Y.%m.%d')
                    except:
                        print('리스트 파싱 과정에서 오류 발생')
                        break

                    if article_date != datetime.strptime(date, '%Y%m%d'):
                        # print('다음 기사는 날짜가 다르므로 무시합니다', pd.to_datetime(article_date),pd.to_datetime(date))
                        elem_index += 1
                        continue

                    # print('추가: ', sid, element.text)

                    if sid == '정치':
                        result_list['정치'].add(element.text)
                    elif sid == '경제':
                        result_list['경제'].add(element.text)

                    elem_index += 1

    result_list = {'정치': list(result_list['정치']), '경제': list(result_list['경제'])}
    print(company, '끝')
    return result_list


if __name__ == '__main__':
    start_parse('조선일보')
