import requests
import bs4
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pymysql
# 将需要获取历史价格时间的数据放入列表传入，会将所有成功获取价格的数据存入数据库
# 在中途难以获取数据的商品链接或名称会存入 fail_web 列表中
# 后在原列表中将fail_web 列表中的数据清除或者从fail_web列表中抓取有效数据存入数据库

def get_database():
    dict = {}
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')  # GOODS_ID like %s', ('15%')
    cur.execute('select GOODS_ID,GOODS_URL from goods_detail where GOODS_ID like %s', ('21%') )
    #where GOODS_ID like %s', ('38%')
    for i in cur:
        dict[i[0]] = i[1]
    cur.close()
    conn.close()
    print(dict)
    return dict


fail_web = []
def get_url(basic_web_dict):

    deal_web_dict = {}
    # 不弹窗
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--disable-gpu')
    #设置请求头部
    chrome_option.add_argument('lang=zh_CN.UTF-8')
    chrome_option.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"')
    # 配置文件
    chrome_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver, options=chrome_option)
    # 开始进入
    driver.get('http://p.zwjhl.com/price.aspx?url=')
    time.sleep(2)
    for goods_id in basic_web_dict:
        try:
            print("--------正在获取id为{0}的商品连接---------".format(goods_id))
            driver.find_element_by_id('url').clear()
            driver.find_element_by_id("url").send_keys(basic_web_dict[goods_id])
            time.sleep(0.5)
            driver.find_element_by_class_name("btn").send_keys(Keys.ENTER)
            time.sleep(0.5)
            urls = driver.current_url
            print(urls)
            deal_web_dict[goods_id] = urls
            time.sleep(0.5)
        except:
            print("获取{0}的链接失败".format(basic_web_dict[goods_id]))
            fail_web.append(basic_web_dict[goods_id])

    driver.quit()
    return deal_web_dict


def url_open(url):
    try:
        header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'Accept-Language':'zh-CN,zh;q=0.9',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        res = requests.get(url,headers = header)
        soup = bs4.BeautifulSoup(res.content, 'html.parser')
        return soup
    except:
        print("获取解析网页源代码失败")
        fail_web.append(url)

# def parser(html):
#     try:
#         soup = bs4.BeautifulSoup(html.content, 'html.parser')
#         return soup
#     except :
#         print("解析错误")
def transform_time(url_time):
    times = float(url_time)
    timestamp = float(times / 1000)
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime


def find_content(soup):
    #获取商品时间和价格
    try:
        dict = {}  #获取商品的时间和价格
        content = []  #获取商品名称和字典价格
        info = soup.find_all('script')[-1].get_text().replace('$(document).ready(function () { flotChart.chartNow(','').replace(", 'pc');   });","")
        # 获取商品名称
        goods_name = soup.find_all('div', {'style': 'float: right; width: 100%;'})[0].find('h1').get_text().replace(
            '\n', '').strip()
        content.append(goods_name)
        # #获取商品时间
        # tmp = '\[Date\.UTC\((.+?)\)'
        # goods_time = re.findall(tmp,info)
        # #获取商品价格
        # tmp1 = '\),(.+?)\]'
        # goods_price = re.findall(tmp1,info)
        # for i in range(len(goods_time)):
        #     dict[goods_time[i]] = goods_price[i]

        # 新的获取商品时间与价格的方式
        tmp = r'\[(.+?),"'
        goods = re.findall(tmp, info)
        for i in range(len(goods)):
            temp = goods[i].split(",")
            dict[transform_time(temp[0])] = temp[1]
        print(dict)
        content.append(dict)
        time.sleep(0.5)
        return content
    except:
        print("获取商品内容失败")


def Connect_Database(all_content):
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')
    print(all_content)
    for goods_id in all_content:
        # 将列表打散成字典取数据
        temp = all_content[goods_id][1]
        for time in temp:
            cur.execute('select GOODS_ID,TIMES from goods_his WHERE GOODS_ID = %s and TIMES = %s',(goods_id,time))
            data = cur.fetchall()
            if data == ():
                cur.execute('insert into goods_his(GOODS_ID,TIMES,PRICE) values(%s,%s,%s)',(goods_id,time,temp[time]))
        print("正在插入id为{0}的商品信息".format(goods_id))
        # 提交
        conn.commit()
    cur.close()
    conn.close()

#创建 插入数据库的 list
def insertDBList(content,good_id):
    DBlist = []
    for i in content[1]:
        temp = []
        temp.append(good_id)
        temp.append(i)
        temp.append(content[1][i])
        DBlist.append(temp)
    print('这是DBList:',DBlist)
    return DBlist

#返回 两个表对比 返回有差异的商品ID
def verify(dict):
    ver = []
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    sql = 'select distinct GOODS_ID from goods_his'
    cur.execute(sql)
    for row in cur.fetchall():
        ver.append(row[0])
    conn.commit()
    cur.close()
    conn.close()
    ver2 = []
    for i in dict:
        ver2.append(i)
    goodsId = list(set(ver2).difference(set(ver)))
    newDict = {}
    for goods in goodsId:
        newDict[goods] = dict[goods]
    print("newDICT",newDict)
    return newDict

def insertDB(DBlist):
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    sql = 'INSERT INTO goods_his VALUES (%s,%s,%s)'
    cur.executemany(sql,DBlist)
    conn.commit()
    cur.close()
    conn.close()

def Primary():
    all_content = {}
    # 防止断片
    deal_web_dict = 'null'
    soup = 'null'
    content = 'null'
    #填写京东等商品页面网址
    website = "https://item.jd.com/100004286189.html"
    web_list  = ['http://item.jd.com/3491212.html','http://item.jd.com/100007395976.html']
    goods_id_list = []
    DBlist = []
    dict = get_database()  #从数据库中获取商品id和url 存入字典
    dict = verify(dict)
    deal_web_dict = get_url(dict)
    if deal_web_dict != 'null':
        print(deal_web_dict)
        for goods_id in deal_web_dict:
            goods_id_list.append(goods_id)
            print('--------------正在获取商品id为{0}的商品时间和价格------------'.format(goods_id))
            soup = url_open(deal_web_dict[goods_id])
            if soup != 'null':
                content = find_content(soup)
                if content != None:
                    all_content[goods_id] = content
                    DBlist = DBlist + insertDBList(content,goods_id)
                    print('-----成功获取，即将获取下一个，请稍等-----------')
                else:
                    temp_list_qw = []
                    content =["null",{"null":"null"}]
                    all_content[goods_id] = content
                    temp_list_qw.append(goods_id)
                    temp_list_qw.append('null')
                    temp_list_qw.append('null')
                    DBlist.append(temp_list_qw)
                    print('-----------该数据获取失败，已将其设为空值---------------')
    print("DBlist :",DBlist)
    print("ALL_CONTENT",all_content)
    print('未成功获取的链接:')
    print(fail_web)
    print('---------将已经获取的数据插入数据库----------')
    insertDB(DBlist)
    #Connect_Database(all_content)
    print('---------成功插入数据库---------------')


if __name__ == "__main__":
    Primary()