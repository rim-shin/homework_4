import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# 타겟 URL을 읽어서 HTML를 받아오고, (고정작업/복붙가능)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
music = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
count = 0

# music (tr들) 의 반복문을 돌리기
for music_list in music:
    # music 안에 a 가 있으면,
    music_title = music_list.select_one('td.info > a.title.ellipsis')
    music_singer = music_list.select_one('td.info > a.artist.ellipsis')
    count += 1

    if music_title is not None:
        # a의 text를 찍어본다.
        title = music_title.text.strip()
        singer = music_singer.text

        doc = {
            'rank': count,
            'title': title,
            'singer': singer
        }

        db.music.insert_one(doc)