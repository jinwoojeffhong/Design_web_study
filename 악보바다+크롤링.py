
# ###  크롤링 코드


from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from tqdm import tqdm

import pandas as pd
import numpy as np
import json

## 크롤링한 정보를 담을 Empty array 만들기

final_array = np.empty([0,7], dtype = object)

## 크롤링코드
for page in tqdm(range(1,101)) :


    ## 크롤링할 노래 리스트 정보 긁어오기
    url = "http://www.akbobada.com/ajaxPartgList.html?pageIndex={}&order1=&order2=&order3=&catCode=02&groupCode=12&searchText="
    html = urlopen(url.format(page))
    akbo = json.load(html)


    # 페이지의 크롤링 정보를 담을 임시array 만들기
    temp_array = np.empty([30,7], dtype = object)


    for num in range(len(akbo)) :
        try :
            ## 곡명,아티스트,앨범 가져오기
            temp_array[num, 0] = akbo[num]["AK_NAME"]
            temp_array[num, 1] = akbo[num]["ARTISTLIST"]
            temp_array[num, 2] = akbo[num]["ALBUM_NAME"]


            ## 파트, 설명, Key(조), 페이지 가져오기
            song_url = "http://www.akbobada.com/musicDetail.html?musicID={}&p=1"
            song_num = str(akbo[num]["AKBO_ID"])
            song_html = urlopen(song_url.format(song_num))
            song_page = bs(song_html,"lxml")


            for i, child in enumerate(song_page.find("table").findAll("tr")) :

                ##크롤링 알고리즘 : "피아노" container 를 찾으면 바로 밑의 항목들의 정보를 크롤링해오는 방식
                if ("피아노" in child.text.strip().split()) & (len(child.text.strip().split())==1):

                    info_list = song_page.find("table").findAll("tr")[i+1].text.strip().split()

                    temp_array[num,3] = info_list[0] + info_list[1] #피아노 3단
                    temp_array[num,4] = info_list[3] #설명
                    temp_array[num,6] = info_list[-5] + info_list[-4] #페이지
                    if info_list[5].find(")") >= 0 :
                        temp_array[num,5] = info_list[4] +info_list[5]
                    else :
                        temp_array[num,5] = info_list[4]  #key(조)



        except KeyError :
            continue


    final_array = np.concatenate([final_array,temp_array])
result = pd.DataFrame(final_array, columns = [["곡명", "아티스트", "앨범", "파트", "설명", "Key(조)" ,"페이지"]])

