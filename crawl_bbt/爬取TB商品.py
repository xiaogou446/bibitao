import requests
import bs4
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pymysql
import urllib.request

def open_url(url):
      try:
        header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'accept-language':'zh-CN,zh;q=0.9',
                  'cookie':'thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; _uab_collina=158139921728220681549964; cna=+ibIFv0D3nkCAXAOQrEc4DFn; uc3=vt3=F8dBxdsbAtjAVkl9r1g%3D&nk2=sym591k%3D&id2=UU6hR8yqRPIYBw%3D%3D&lg2=UtASsssmOIJ0bQ%3D%3D; lgc=%5Cu5C0F%5Cu5237a; uc4=nk4=0%40sVYZIGuNBN5cksqfxIg7JA%3D%3D&id4=0%40U2xsB%2BgrhTCr4YuY%2BfM0kW%2BF1UO7; tracknick=%5Cu5C0F%5Cu5237a; _cc_=UtASsssmfA%3D%3D; tg=0; enc=R9SD%2FaDPY4bbthKg%2BCGCQ967rdZnuC8KcOEgknYHOMdJGoldjJB5tQTbiSnwl8aGBjxj9fWqeQshnYcNqkTzwA%3D%3D; mt=ci=1_1; uc1=cookie14=UoTUO8RDICr9Jw%3D%3D; v=0; t=b8e6bb68c31be8209b8351dd3dba31b9; cookie2=5d09246d100eeee7c8f1605e83e066b7; _tb_token_=e77b5e79ee33a; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; _samesite_flag_=true; JSESSIONID=563C76F2A077C3A563DFA05622D5887B; l=cBSebLgeQbN9dbBXKOfZ-urza77tWIdb8sPzaNbMiICPOvfycQl1WZVmuTY2CnGVKstWX3W-27a0BzYH7ydq0-Y3L3k_J_f..; isg=BO3ttCQPTw9qNCtgezoQr6BO_IlnSiEcQs63kC_z0ATEpgxY4ZsH7CF0kHpAJjnU'}
        res = urllib.request.Request(url,headers=header)
        html = urllib.request.urlopen(res).read().decode('utf-8')
        return html
      except:
          print('网页打开失败')

def parser(html):
    try:
        soup = bs4.BeautifulSoup(html,'html.parser')
        return soup
    except:
        print('解码失败')

def find_net(soup):
    try:
        one_page = []
        script_content = soup.find_all('script')[-2].text
        r='detail_url\":\"//detail.tmall.com/item.htm\?id(.+?)\",\"view'
        goods_temp=re.findall(r,script_content)
        for i in goods_temp:
            Chi_goods = i.encode('utf-8').decode('unicode_escape')
            Chi_url = Chi_goods.split("&")[0]
            goods_url = 'https://detail.tmall.com/item.htm?id'+Chi_url
            one_page.append(goods_url)
        return one_page
    except:
        print("没有找到url  可能url被验证了")

#存入数据库
def store_database(final):
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')
    cur.execute('select max(GOODS_ID) from goods_detail where GOODS_ID like %s', ('96%'))
    data = cur.fetchall()
    if str(data[0][0]) == 'None':
        num = 96001
    else :
        num = int(data[0][0])
    for one_list in final:
        for one_goods in one_list:
            #开始存储
            cur.execute('select * from goods_detail where goods_url = %s ', (one_goods))
            data = cur.fetchall()
            if data == ():
                num = num + 1
                cur.execute('insert into goods_detail(GOODS_ID,GOODS_URL) values(%s,%s)',(num,one_goods))


    conn.commit()
    cur.close()
    conn.close()
    print('-----恭喜！已经成功存储--------')

#https://s.taobao.com/search?q=%E6%91%86%E6%B8%A1%E8%80%85%E5%B9%B3%E6%9D%BF&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200212&ie=utf8
def Primary():
    all_page =[]
    for i in range(10):
        print("正在爬取第{0}页".format(i))
        url="https://s.taobao.com/search?q=%E6%91%86%E6%B8%A1%E8%80%85%E5%B9%B3%E6%9D%BF&s={0}".format(44*i)
        html = open_url(url)
        soup = parser(html)
        one_page = find_net(soup)
        print(one_page)
        if one_page == None:
            one_page=[]
        all_page.append(one_page)
    if all_page[0] == "":
        print("爬取失败 被拦截")
    else:
        print(all_page)
        store_database(all_page)

if __name__ == "__main__":
    Primary()


