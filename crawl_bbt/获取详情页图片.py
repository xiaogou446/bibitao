import urllib.request
import bs4
import re
import requests
import pymysql
import time
from urllib.request import urlretrieve
#为了获取商品详情页的小图与大图

def get_url():
    url = []
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')   #like %s', ('11%')
    cur.execute('select GOODS_URL from goods_detail where GOODS_ID like %s', ('11%'))
    # data = cur.fetchall()
    # print(data)
    for i in cur:
        url.append(i[0])
    # conn.commit()
    # print(len(urls))
    cur.close()
    conn.close()
    return url

def open_url(url):
    try:
        header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'accept-language':'zh-CN,zh;q=0.9'}
        res = urllib.request.Request(url,headers=header)
        html = urllib.request.urlopen(res).read().decode('gbk')
        return html
    except:
        print("打开网页失败")

def parser(html):
    try:
        soup = bs4.BeautifulSoup(html,'html.parser')
        return soup
    except:
        print('解析网页失败')

def find_img(soup):
    try:
        img_dict={}
        ul_lh = soup.find_all('ul',{'class':'lh'})[1]
        imgs = ul_lh.find_all('img')
        for i in range(3):
            small_img = 'http:'+imgs[i].get('src')
            if 's54x54' in small_img:
                big_img = small_img.replace('com/n5/s54x54','com/n1/s450x450')
            else:
                big_img = small_img.replace('com/n5/', 'com/n1/')
            img_dict[small_img] = big_img
        return img_dict
    except:
        print('无法获取该图片地址')

def store_database(all_list):
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')
    for one_url_img in all_list:
        for url in one_url_img:
            cur.execute('select GOODS_ID from goods_detail where GOODS_URL = %s',(url))
            data = cur.fetchall()
            goods_id = data[0][0]
            i=1
            for small_img in one_url_img[url]:
                big_img= one_url_img[url][small_img]
                small_img_name= 'E:\detail_img/detailSmall'+str(i)+'Img' + str(goods_id) + '.jpg'
                big_img_name = 'E:\detail_img/detailBig'+str(i)+'Img' + str(goods_id) + '.jpg'
                urlretrieve(small_img, 'E:\detail_img/detailSmall'+str(i)+'Img' + str(goods_id) + '.jpg')
                urlretrieve(big_img, 'E:\detail_img/detailBig'+str(i)+'Img' + str(goods_id) + '.jpg')
                cur.execute(
                    'update goods_detail set SMALL_IMG'+str(i)+'= %s,BIG_IMG'+str(i)+' =%s where goods_id = %s',
                    (small_img_name, big_img_name,goods_id))
                i=i+1

            # for small_img2 in one_url_img[url][1]:
            #     small_img2=small_img2
            #     big_img2 = one_url_img[url][0][small_img2]
            # for small_img3 in one_url_img[url][2]:
            #     small_img3=small_img3
            #     big_img3 = one_url_img[url][0][small_img3]
            # small_img1_name = '../imgs/detailSmall1Img' + str(goods_id) + '.jpg'
            # big_img1_name = '../imgs/detailBig1Img' + str(goods_id) + '.jpg'
            # small_img2_name = '../imgs/detailSmall2Img' + str(goods_id) + '.jpg'
            # big_img2_name = '../imgs/detailBig2Img' + str(goods_id) + '.jpg'
            # small_img3_name = '../imgs/detailSmall3Img' + str(goods_id) + '.jpg'
            # big_img3_name = '../imgs/detailBig3Img' + str(goods_id) + '.jpg'
            # urlretrieve(small_img1, small_img1_name)
            # urlretrieve(big_img1, big_img1_name)
            # urlretrieve(small_img2, small_img2_name)
            # urlretrieve(big_img2, big_img2_name)
            # urlretrieve(small_img3, small_img3_name)
            # urlretrieve(big_img3, big_img3_name)
            #
            # cur.execute('update goods_detail set SMALL_IMG1= %s,BIG_IMG1 =%s,SMALL_IMG2= %s,BIG_IMG2= %s,SMALL_IMG3= %s,BIG_IMG3= %s where goods_id = %s',(small_img1,big_img1,small_img2,big_img2,small_img3,big_img3,goods_id))
    conn.commit()
    cur.close()
    conn.close()

def Primary(url):
    url_img_dict={}
#    url = 'https://item.jd.com/56166176873.html'
    html = open_url(url)
    soup = parser(html)
    img_dict = find_img(soup)
    if img_dict ==None:
        print("该图片无法获取")
    else:
        url_img_dict[url]= img_dict
        return url_img_dict

if __name__ == "__main__":
    all_list= []
    # final_list =[]
    url = get_url()
    if url == None:
        print("无法从数据库中获取数据")
    else:
        num = len(url)
        if num != 'null':
            for i in range(len(url)):
                print("-------正在获取第{0}个商品的数据,一共{1}个-----------".format(i,num))
                url_img_dict=Primary(url[i])
                if url_img_dict != None:
                    all_list.append(url_img_dict)
                    time.sleep(0.5)
            print(all_list)
            store_database(all_list)
        else:
            print('从数据库中获取数据失败')
    # url_img_dict = Primary()
    # all_list.append(url_img_dict)
    # print(all_list)
    # store_database(all_list)