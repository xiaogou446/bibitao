import urllib.request
import bs4
import re
import requests
import pymysql
import time
import  json
import  datetime

def get_url():
    #{96002: ['https://detail.tmall.com/item.htm?id=604707028216', '天猫'], 96003: ['https://detail.tmall.com/item.htm?id=600166291798', '天猫']}
    dict={}
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')  # GOODS_ID like %s', ('15%')
    cur.execute('select GOODS_ID,GOODS_URL,source from goods_detail ' )
    for i in cur:
        dict[i[0]] = [i[1],i[2]]
    cur.close()
    conn.close()

    print(dict)
    return dict

def open_url(url):
    try:
        header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'accept-language':'zh-CN,zh;q=0.9',
                  'cookie':'__utmc=188916852; Hm_lvt_7705e8554135f4d7b42e62562322b3ad=1584244530,1584259206; __utma=188916852.1598870400.1584244530.1584244530.1584259207.2; __utmz=188916852.1584259207.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; PHPSESSID=232loboceo4on72j1mptjeueh1; GWD_ACCESS_TOKEN=ceccf41414e74e658fa0a58b4b7ff8d1; amvid=47eda0626a11845038c98911a4ed546d; __utmb=188916852.15.9.1584259333997; Hm_lpvt_7705e8554135f4d7b42e62562322b3ad=1584259525'}
        res = urllib.request.Request(url,headers=header)
        html = urllib.request.urlopen(res,timeout=3).read().decode('gbk')
        return html
    except:
        print("打开网页失败")

def get_JD_code(url):
    try:
        id = re.findall(r'jd\.com/(.*?)\.html', url)[0]
        urls = "https://www.gwdang.com/trend/data_www?dp_id={0}-3&show_prom=true&v=2&get_coupon=1&price=".format(id)
        print(urls)
        result = open_url(urls)
        #print(result)
        result = json.loads(result)
        fina_price = str(result.get("series")[0].get("data")[-1].get('y'))
        price = fina_price[:-2] + ".00"
        return price

    except:
        print("无法获取数据")


def get_TM_code(url):
    try:
        id= url.split("id=")[1]
        urls = "https://www.gwdang.com/trend/data_www?dp_id={0}-83&show_prom=true&v=2&get_coupon=0&price=".format(id)
        print(urls)
        result = open_url(urls)
        #print(result)
        result = json.loads(result)
        fina_price = str(result.get("series")[0].get("data")[-1].get('y'))
        price = fina_price[:-2] + ".00"
        return price

    except:
        print("无法获取数据")


dict={}
def Primary(key,url_list):

    price = 'null'

    if url_list[1]=='京东':
        price = get_JD_code(url_list[0])
        print(price)
        if price != None:
            dict[key] = price
        else:
            dict[key] = 'null'
    else:
        price = get_TM_code(url_list[0])
        print(price)
        if price !=None:
            dict[key] = price
        else:
            dict[key] = 'null'

def store_database(dict):
    times = datetime.datetime.now().strftime("%Y-%m-%d")
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')
    for key in dict:
        print("正在存{0}的商品".format(key))
        cur.execute('update goods_detail set GOODS_PRICE = %s where GOODS_ID = %s',(dict[key],key))
        try:
            cur.execute('insert into goods_his values(%s,%s,%s)',(key,times,dict[key]))
        except:
            pass
        #cur.execute('insert into goods_his values(%s,%s,%s)',())

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    num = 'null'
    #dict_url ={32017: ['https://item.jd.com/30141057388.html', '京东'], 96003: ['https://detail.tmall.com/item.htm?id=600166291798', '天猫']}
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
