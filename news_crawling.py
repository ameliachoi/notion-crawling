from notion.client import *
from notion.block import *

# 키워드 뉴스 크롤링 하기
from bs4 import BeautifulSoup
import requests
import datetime

# 키워드 별로 크롤링 하기
def news():
    keyword = '비트코인'
    now = datetime.datetime.now()
    now_date = now.strftime('%Y.%m.%d')
    now_date2 = now.strftime('%Y%m%d')

    news_list = []

    for page_number in range(3): # 한 페이지 당 기사 10개
        url_format = "https://search.naver.com/search.naver?&where=news&query={}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds={}&de={}&docid=&nso=so:r,p:from{}to{},a:all&mynews=0&cluster_rank=27&start={}"
        req = requests.get(url_format.format(keyword, now_date, now_date, now_date2, now_date2, str(page_number)),
                           headers={'User-Agent': 'Mozilla/5.0'})
        sp = BeautifulSoup(req.text, 'html.parser')  # 파싱하여 원하는 데이터만 가져오게 html 저장

        sources = sp.select('div.group_news > ul.list_news > li div.news_area > a')

        for source in sources:
            title = source.attrs['title']
            url = source.attrs['href']

            crawling_news = {
                '기사 제목' : title,
                '키워드' : keyword,
                'url' : url,
                '크롤링 날짜' : str(now_date)
            }

            news_list.append(crawling_news)

    return news_list


token = "토큰 번호 입력하기"
url = "url 번호 입력하기"

# client 만들고 페이지 정보 가져오기
client = NotionClient(token_v2=token)
page = client.get_collection_view(url)

news = news()

for onenews in news:
    row = page.collection.add_row()
    row.title = onenews['기사 제목']
    row.crawlingdate = onenews['크롤링 날짜']
    row.keyword = onenews['키워드']
    row.url = onenews['url']