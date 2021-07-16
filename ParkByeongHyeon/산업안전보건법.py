import requests
from urllib.request import urlopen
from urllib.parse import urlencode,unquote,quote_plus
import urllib
import lxml
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re

# 법령 XML 상세조회 (시행기준. target=eflaw)

#기본 url
url_base = " http://www.law.go.kr/DRF/lawService.do"

#조회 url 세부 설정
user_id = 'bmsong' #open API ID (bmsong@kau.ac.kr의 아이디 부분)
target = "eflaw" #법령 조회시
MST = "218289" #ID 또는 MST #산업안전보건법 MST 218289
#ID = "001766" 
            #ID 산업안전보건법 법령ID 001766 (설명에는 ID로 조회하면 현행법령이 조회된다는데, 
            #target을 eflaw로 하면 ID로 요청해도, MST로 요청해도 같은 것 같다.
Type = "XML" #출력 형태 : HTML 또는 XML

url_sub = "?" +\
        "OC=" + user_id +\
        "&target=" + target +\
        "&MST=" + MST +\
        "&type=" + Type

#최종 url
url = url_base + url_sub

response = requests.get(url)

#(1) response.text 사용하는 방법
#soup = BeautifulSoup(response.text.encode('utf-8'), 'lxml-xml') #lxml-xml -> lxml 추가 설치 필요(Beautifulsoup과 별도로 설치)

#(2) response.content 사용하는 방법
soup = BeautifulSoup(response.content, 'lxml-xml') #lxml-xml -> lxml 추가 설치 필요(Beautifulsoup과 별도로 설치)


data = soup.find_all('조문단위')

info = []
for i in data:
    detail = {}
    if i.find("조문여부").get_text() == "조문":
        조문제목 = i.find("조문내용").get_text().strip().split(")")[0]+")"
        detail["조문제목"] = 조문제목
        
        조문내용 = i.find("조문내용").get_text().strip()[len(조문제목):-1].strip()
        detail["조문내용"] = 조문내용
        info.append(detail)

        항문내용 = []
        if i.find("항내용"):
            for j in i.find_all("항내용"):
                항문내용.append(j.get_text().strip())
        detail["항문내용"] = 항문내용

                
                
                
for i in info:
    print(i)

                

            
        
        

