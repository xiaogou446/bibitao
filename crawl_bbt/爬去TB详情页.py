import urllib.request
import bs4
import re
import requests
import pymysql
import time
import json
from urllib.request import urlretrieve

def get_url():
    dict={}
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')  # GOODS_ID like %s', ('15%')
    cur.execute('select GOODS_ID,GOODS_URL from goods_detail where GOODS_ID like "96%"' )
    for i in cur:
        dict[i[0]] = i[1]
    cur.close()
    conn.close()
    print(dict)
    return dict



def open_url(url):
    try:
        header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'accept-language':'zh-CN,zh;q=0.9',
                  'cookie':'hng=CN%7Czh-CN%7CCNY%7C156; cna=+ibIFv0D3nkCAXAOQrEc4DFn; lid=%E5%B0%8F%E5%88%B7a; enc=R9SD%2FaDPY4bbthKg%2BCGCQ967rdZnuC8KcOEgknYHOMdJGoldjJB5tQTbiSnwl8aGBjxj9fWqeQshnYcNqkTzwA%3D%3D; cq=ccp%3D1; t=b8e6bb68c31be8209b8351dd3dba31b9; uc4=nk4=0%40sVYZIGuNBN5cksqfxIg7JA%3D%3D&id4=0%40U2xsB%2BgrhTCr4YuY%2BfM0kW%2BF1UO7; _tb_token_=e77b5e79ee33a; cookie2=5d09246d100eeee7c8f1605e83e066b7; _m_h5_tk=61e2baaa25c0979bc7b8d7c59d93f055_1581507530698; _m_h5_tk_enc=8cb319df07b4bd0eee69e4051821d8fe; pnm_cku822=098%23E1hvJpvUvbpvUvCkvvvvvjiPn2zZ1jDURLMOAjivPmP90jimPFFpAj1hPFMZ1jr82QhvCvvvMMGCvpvVvUCvpvvvKphv8vvvphvvvvvvvvCVB9vvvcyvvhXVvvmCWvvvByOvvUhwvvCVB9vv9BAivpvUvvCCWJL3bOKEvpvVvpCmpYsymphvLUHbmpyafXKK53Dz7txreuTJdB61D764diTAVArl%2FCGXV3ODNr3l53e4eeO2famKHd8rJoL6%2Ff8rVTt%2Bm7zOdigXe5xLD764d34AVAGtvpvhvvCvp8wCvvpvvhHh; isg=BD09y4-FPx8eZJtyKfCh2Kf2TJk32nEskr7nYP-CfBTDNl1oxyv8_UPs4Gpwtonk; l=cBgH5VHHQYkOoYXLBOCwnurza77tIIRAguPzaNbMi_5BF6Y1AKQOoSbzEFv6cjWd9pTB4Tn8Nr29-etkjpa1CL1P97RN.'}
        res = urllib.request.Request(url,headers=header)
        html = urllib.request.urlopen(res,timeout=3).read().decode('gbk')
        return html
    except:
        print("打开网页失败")

def parser(html):
    try:
        soup = bs4.BeautifulSoup(html,'html.parser')
        return soup
    except:
        print('解析网页失败')

def find_content(soup):
    try:
        content_code = []

        #爬取3 id
        con_script = soup.find_all('script')[4].text
        r = 'itemId:\"(.+?)\",sellerId:\"(.+?)\",shopId:\"(.+?)\"'
        code = re.findall(r,con_script)
        itemId = code[0][0]
        sellerId = code[0][1]
        shopId = code[0][2]
        content_code.append(itemId)
        content_code.append(sellerId)
        content_code.append(shopId)

        #爬取评分
        degree = soup.find_all('div',{'class':'main-info'})[0]
        goods_degree = degree.find_all('span',{'class':'shopdsr-score-con'})[0].text
        goods_degree = int(float(goods_degree)*20)
        goods_degree = str(goods_degree)+'%'
        content_code.append(goods_degree)

        #爬取商家
        shop = soup.find_all('a',{'class':'slogo-shopname'})[0].strong.text
        content_code.append(shop)


        print(content_code)
        return content_code
    except:
        print('无法找到内容')

def get_code(list):
    try:
        content_list = []
        url_P = 'https://ald.taobao.com/recommend.htm?refer=&_ksTS=&callback=jsonp443&recommendItemIds={}&needCount=&shopId={}&sellerID={}&appID=03130&isTmall=true&moduleId'.format(list[0],list[2],list[1])
        new_html = requests.get(url_P).text

        r = 'jsonp443\((.+?)\)'
        deal_str = re.findall(r, new_html)[0]
        json_str = json.loads(deal_str)
        img = json_str.get("itemList")[0].get("img")
        title = json_str.get("itemList")[0].get("title")
        eva_temp = json_str.get("itemList")[0].get("commentNum")
        if eva_temp >= 10000:
            eva = eva_temp / 10000
            evas1 = str(eva).split(".")[0] + "." + (str(eva).split(".")[1])[0:1]
            eva = evas1 + "万+"
            print(eva)
        elif eva_temp<10:
            eva = str(eva_temp)
            print(eva)
        else:  # 3215
            lens = len(str(eva_temp)) - 1
            num_t = 10 ** lens
            evas1 = eva_temp / num_t
            eva = str(int(evas1) * num_t) + "+"
            print(eva)
        price = json_str.get("itemList")[0].get("price")
        content_list.append(img)
        content_list.append(title)
        content_list.append(eva)
        content_list.append(price)
        content_list.append(list[3])
        content_list.append(list[4])


        return content_list
    except:
        print("无法获取数据")

def store_database(dict):
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')
    for key in dict:
        print("正在存{0}的商品".format(key))
        store_name = 'E:\search_img/searchImg' + str(key) + '.jpg'
        #img_name  存在电脑的路径 需修改
        img_name = 'D:\pycharm\imgs/searchImg' + str(key) + '.jpg'
        cur.execute('update goods_detail set SEARCH_IMG= %s,GOODS_TITLE =%s,GOODS_EVA = %s,GOODS_PRICE = %s,GOODS_DEGREE = %s,shop = %s where GOODS_ID = %s',(store_name,dict[key][1],dict[key][2],dict[key][3],dict[key][4],dict[key][5],key))
        try:
            urlretrieve('https:'+dict[key][0], img_name)
        except:
            pass
    conn.commit()
    cur.close()
    conn.close()
dict = {}
fail_list = []
def Primary(key,url):
    html = 'null'
    soup = 'null'
    list = 'null'
    content_list = 'null'

    html = open_url(url)
    if html != 'null':
        soup = parser(html)
    if soup != 'null':
        list = find_content(soup)
    if list != 'null':
        content_list =get_code(list)
        print(content_list)
        if content_list != None:
            dict[key] = content_list
        else:
            dict[key] =['null','null','null','null','null','null']


    # if html == 'null' or soup =='null' or list =='null' or content_list == 'null':
    #     print(url +'无法成功爬取')
    #     fail_list.append(url)



if __name__ == "__main__":
    num = 'null'
    #dict_url ={61002: 'https://detail.tmall.com/item.htm?id=609asasasa'}
    dict_url = get_url()
    num = len(dict_url)
    if num != 'null':
        for key in dict_url:
            print("-------正在获取{0}商品的数据,一共{1}个-----------".format(key,num))
            #url='https://detail.tmall.com/item.htm?id=606179965663'
            Primary(key,dict_url[key])
            time.sleep(0.5)
    print(dict)

    store_database(dict)
    # else:
    #     print('从数据库中获取数据失败')



