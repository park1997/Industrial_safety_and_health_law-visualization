# 산업안전보건법 보편적 이해를 위한 법령 시각화 연구 (A study on the visualization of laws for universal understanding of the Occupational Safety and Health Act.)
## Project 
산업안전보건법 보편적 이해를 위한 법령 시각화 연구를 위한 유사조항 네트워크 시각화 분석

## Packages
1. Doc2Vec
2. Word2Vec
3. sklearn(TfidfVectorizer,CountVectorizer,cosine_similarity,euclidean_distances)
4. Pandas
5. openpyxl
6. BeautifulSoup
7. lxml
8. re
9. koNLPy(Mecab,Okt)
10. WordCloud
11. Matplotlib
12. Seaborn

## Research
### 1. 데이터 수집
1. '국가법령정보센터' Api권한 획득
![스크린샷 2021-11-09 오후 1 34 10](https://user-images.githubusercontent.com/73048180/140862724-5a2ef540-e063-4a56-bfc2-0fd8135a9ed1.png)
2. 조문 단위로 산업안전보건법, 건설기술진흥법, 위험물안전관리법, 전기안전관리법, 화학물질관리법 Crawling
```
data = soup.find_all('조문단위')
df_info = pd.DataFrame()
info = []
key = []
for i in data:
    info_str = ""
    if i.find("조문여부").get_text() == "조문":
        info_str += i.조문내용.get_text().strip() + ' '
        if i.항:
            hang_nums = i.find_all("항번호")
            ho_nums = i.find_all("호번호")
            if not i.find("항내용") :
                for idx, p in enumerate(i.find_all("호내용")):
                    info_str += p.get_text().split(ho_nums[idx].get_text())[1].strip() + ' '
            else:
                for hang_idx , k in enumerate(i.find_all("항내용")):
                    info_str += k.get_text().strip().split(hang_nums[hang_idx].get_text())[1].strip() + ' '
                for ho_idx , j in enumerate(i.find_all("호내용")):
                    info_str += j.get_text().strip().split(ho_nums[ho_idx].get_text())[1].strip() + ' '
        info.append(info_str)
        key.append(i['조문키']+"2")

df_info["키"] = key
df_info["조내용"] = info

df_info
```
![스크린샷 2021-11-09 오후 1 39 50](https://user-images.githubusercontent.com/73048180/140863305-5d818dcb-3192-4b46-92cf-7794479095cb.png)


### 2. 데이터 전처리 및 구조화
1. 텍스트 마이닝
- 비정형 텍스트 데이터로부터 정보를 추출하고 가공하기 위해 자연어처리(Natural Language Processing)기술을 적용
- 텍스트를 말뭉치(Corpus)단위로 변환
- Corpus의 Keyword추출
- 문서-키워드 행렬(DTM: Document-Term Matrix)구축

텍스트 마이닝은 Python의 KoNLPy를 사용하였고 「산업안전보건법」 의 raw data의 상의 용어 정보는 다음 워드 클라우드(Word Cloud)와 같다.

<img width="579" alt="스크린샷 2021-11-09 오후 1 45 23" src="https://user-images.githubusercontent.com/73048180/140863864-4a1ac6b4-4b91-48cd-9b9f-aa8d68950c81.png">

「산업안전보건법」과 함께 「건설기술진흥법」, 「화학물질관리법」, 「위험물안전관리법」, 「전기안전 관리법」을 통합하여 많이 포함된 용어는 다음과 같다. 

<img width="548" alt="스크린샷 2021-11-09 오후 1 50 56" src="https://user-images.githubusercontent.com/73048180/140864394-fbe651d9-5049-44a2-b0da-98a425638c19.png">

3. 워드 임베딩(Word Embedding)
- CountVector
- TF-IDF(Term Frequency-Inverse Document Frequency)
- Word2Vec
- Doc2Vec

위 방법론들을 이용하여 문서들의 벡터를 생성.

### 3. 유사도 계산
- 민코프스키 거리(Minkowski distance)
- 맨하튼 거리(Manhattan distance)
- 유클리디안 거리 (Euclidean distance)
- 코사인 유사도(cosine similarity)

Cosine Similarity은 계산도 용이하고, 각 벡터 간의 쌍대비교로 상대적인 거리를 측정할 수 있다는 장점이 있다.

### 4. 유사조항 네트워크 시각화
Algorithm은 TF-IDF를 사용함.
- TF-IDF는 법령 측성 상 자주 반복되는 단어의 가중치를 최대한 줄이기 위하여 사용하였음
- 각 조항들간 유사도를 Cosine Similarity를 바탕으로 네트워크로 연결

아래 그림은 안전보건 관련 법령 간 유사 관계를 나타내는 네트워크이다.
<img width="622" alt="스크린샷 2021-11-09 오후 2 02 53" src="https://user-images.githubusercontent.com/73048180/140865541-80ea87b7-0246-47b0-9989-d8e439f67aef.png">

### 5. 유사조항 도출

```
# cosine similarity 값으로 
# x조와 가장 비슷한 조를 찾기위한 과정
jo_key = 750011
jo = key.index(jo_key)
y_cosine = cosine_result_df[jo]
dic ={}
for i in range(len(y_cosine)):
    dic[str(posts_key[i])] = y_cosine[i]
dic = get_key(**dic)
# x조와 비슷한 조 찾기 위함
# euclidean distance 를 dic에 씌워 sorting 함(1부터 25위까지)
sorted(dic.items(), key=lambda x: x[1], reverse = True)[0:25]
```
![스크린샷 2021-11-09 오후 2 06 42](https://user-images.githubusercontent.com/73048180/140865868-4f6948bc-0237-4651-92bf-42ede9f757ee.png)

