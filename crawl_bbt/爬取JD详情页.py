import urllib.request
import bs4
import re
import requests
import pymysql
import time


def get_url():
    url = []
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')    #like %s', ('11%')
    cur.execute('select GOODS_URL from goods_detail where GOODS_ID like %s', ('21%'))
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

def find_content(soup):
    try:
        #爬取价格
        content_code = []
        skuId = soup.find('script',{'charset':'gbk'})
        temp = skuId.get_text()
        r = 'skuid: (.+?),'
        skuId = re.findall(r,temp)[0]
        r1 = 'venderId:(.+?),'
        venderId = re.findall(r1,temp)[0]
        r3 = 'cat: \[(.+?)\],'
        cat = re.findall(r3,temp)[0]
        content_code.append(skuId)
        content_code.append(venderId)
        content_code.append(cat)
        return content_code
    except:
        print('无法找到内容')

def get_code(list):
    try:
        content_list = []
        url_P = 'https://c0.3.cn/stock?skuId={}&area=15_1243_1244_0&venderId={}&buyNum=1&choseSuitSkuIds=&cat={}&extraParam={}&fqsp=0&pdpin=&pduid=1569227642996411875776&ch=1&callback=jQuery'.format(list[0],list[1],list[2],'{%22originid%22:%221%22}')
        new_html = requests.get(url_P).text
        print(url_P)
        r4 = r'"p":"(.+?)"'   #价格正则表达式
       # r4 = re.compile(r'')
        price = re.findall(r4,new_html)[0]  #获得价格
        content_list.append(price)

        url_ev = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={0}&callback=jQuery'.format(list[0])
        ev_url = requests.get(url_ev).text #解码评价的数据页面
        r5 = r'"CommentCountStr":"(.+?)"'   #评价正则表达式
        evaluate = re.findall(r5,ev_url)[0]
        content_list.append(evaluate)
        # print(url_P)

        r6 = r'"GoodRateShow":(.+?),'  #好评度的正则表达式
        degree = re.findall(r6,ev_url)[0]
        content_list.append(degree+"%")
        print(content_list)

        return content_list
    except:
        print("无法获取数据")

def store_database(dict):
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')
    for key in dict:
        cur.execute('update goods_detail set goods_price= %s,goods_eva =%s,goods_degree = %s where goods_url = %s',(dict[key][0],dict[key][1],dict[key][2],key))
    conn.commit()
    cur.close()
    conn.close()
dict = {}
fail_list = []
def Primary(url):
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
    if content_list != None:
        dict[url] = content_list
    else:
        content_list=['null','null','null']
        dict[url] = content_list
    if html == 'null' or soup =='null' or list =='null' or content_list == 'null':
        print(url +'无法成功爬取')
        fail_list.append(url)



if __name__ == "__main__":
    num = 'null'
    # final_list =[]
    url = get_url()
    num = len(url)
    if num != 'null':
        for i in range(len(url)):
            print("-------正在获取第{0}个商品的数据,一共{1}个-----------".format(i,num))
            Primary(url[i])
            time.sleep(0.5)
        print(dict)
        store_database(dict)
    else:
        print('从数据库中获取数据失败')



