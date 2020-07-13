import urllib.request
import bs4
import re
import requests
import pymysql
import time


def get_url(goods_id):
    url = []
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')    #like %s', ('11%')
    cur.execute('select GOODS_URL from goods_detail where GOODS_ID like %s', (goods_id))
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

# 产品名称：model
# CPU型号：  cpu
# 运行内存：  running_memory
# 机身存储：  phone_memory
# 主屏幕尺寸：  screen_size
# 电池容量：  battery_cap
# 品牌 ： brand
def find_phone(soup):
    try:
        #爬取价格
        content_list = []
        #tab_con = soup.find_all('div',{'class':'tab-con'})[3]
        #one_item = str(tab_con.find_all('div',{'class','Ptable'})[0])
        one_item = str(soup)
        rModel = '<dt>产品名称</dt><dd>(.+?)</dd>'
        try:
            model = re.findall(rModel,one_item)[0]
        except:
            try:
                rModel='<li title=\'(.+?)\'>商品名称'
                model = re.findall(rModel,one_item)[0]
            except:
                model = '暂无'

        rCpu = '<dt>CPU型号</dt><dd>(.+?)</dd>'
        try:
            cpu = re.findall(rCpu,one_item)[0]
        except:
            cpu='暂无'
        rRuning_memory = '<dt>运行内存</dt><dd>(.+?)</dd>'
        try:
            running_memory = re.findall(rRuning_memory,one_item)[0]
        except:
            running_memory = '暂无'
        rPhone_memory = '<dt>机身存储</dt><dd>(.+?)</dd>'
        try:
            phone_memory = re.findall(rPhone_memory,one_item)[0]
        except:
            phone_memory='暂无'
        rScreen_size = '<dt>主屏幕尺寸（英寸）</dt><dd>(.+?)</dd>'
        try:
            screen_size = re.findall(rScreen_size,one_item)[0]
        except:
            screen_size='暂无'
        rBattery_cap = '<dt>电池容量（mAh）</dt><dd>(.+?)</dd>'
        try:
            battery_cap = re.findall(rBattery_cap,one_item)[0]
        except:
            battery_cap='暂无'

        rBrand = '<dt>品牌</dt><dd>(.+?)</dd>'
        try:
            brand = re.findall(rBrand, one_item)[0]
        except:
            brand = '暂无'

        content_list.append(model)
        content_list.append(cpu)
        content_list.append(running_memory)
        content_list.append(phone_memory)
        content_list.append(screen_size)
        content_list.append(battery_cap)
        content_list.append(brand)
        print(content_list)

        return content_list
    except:
        print('无法找到内容')


## 电脑属性类型
#   型号： model
#   显卡类型 graphics_card  内建GPU
#   CPU型号 cpu
#   内存容量 running_memory
#   硬盘容量 phone_memory
#   屏幕尺寸 screen_size
#   系列  brand
# #
def find_computer(soup):
    try:
        #爬取价格
        content_list = []
        #tab_con = soup.find_all('div',{'class':'tab-con'})[3]
        #one_item = str(tab_con.find_all('div',{'class','Ptable'})[0])
        one_item = str(soup)
        rModel = '<dt>型号</dt><dd>(.+?)</dd>'
        try:
            model = re.findall(rModel,one_item)[0]
        except:
            try:
                rModel = '<li title=\'(.+?)\'>商品名称'
                model = re.findall(rModel, one_item)[0]
            except:
                model = '暂无'

        rGraphics_card = '<dt>显卡类型</dt><dd>(.+?)</dd>'
        try:
            graphics_card = re.findall(rGraphics_card,one_item)[0]
        except:
            try:
                rGraphics_card = '<dt>内建GPU</dt><dd>(.+?)</dd>'
                graphics_card = re.findall(rGraphics_card,one_item)[0]
            except:
                graphics_card='暂无'

        rCpu = '<dt>CPU型号</dt><dd>(.+?)</dd>'
        try:
            cpu = re.findall(rCpu,one_item)[0]
        except:
            cpu = '暂无'

        rRunning_memory = '<dt>内存容量</dt><dd>(.+?)</dd>'
        try:
            running_memory = re.findall(rRunning_memory,one_item)[0]
        except:
            running_memory='暂无'

        rPhone_memory = '<dt>硬盘容量</dt><dd>(.+?)</dd>'
        try:
            phone_memory = re.findall(rPhone_memory,one_item)[0]
        except:
            phone_memory='暂无'

        rScreen_size = '<dt>屏幕尺寸</dt><dd>(.+?)</dd>'
        try:
            screen_size = re.findall(rScreen_size,one_item)[0]
        except:
            screen_size='暂无'

        rBrand = '<dt>系列</dt><dd>(.+?)</dd>'
        try:
            brand = re.findall(rBrand, one_item)[0]
        except:
            brand = '暂无'

        content_list.append(model)
        content_list.append(graphics_card)
        content_list.append(cpu)
        content_list.append(running_memory)
        content_list.append(phone_memory)
        content_list.append(screen_size)
        content_list.append(brand)
        print(content_list)

        return content_list
    except:
        print('无法找到内容')

# 型号：model
# 品牌：  brand
def find_earphone(soup):
    try:
        #爬取价格
        content_list = []
        #tab_con = soup.find_all('div',{'class':'tab-con'})[3]
        #one_item = str(tab_con.find_all('div',{'class','Ptable'})[0])
        one_item = str(soup)
        rModel = '<dt>型号</dt><dd>(.+?)</dd>'
        try:
            model = re.findall(rModel,one_item)[0]
        except:
            try:
                rModel = '<li title=\'(.+?)\'>商品名称'
                model = re.findall(rModel, one_item)[0]
            except:
                model = '暂无'
        rBrand = '<dt>品牌</dt><dd>(.+?)</dd>'
        try:
            brand = re.findall(rBrand, one_item)[0]
        except:
            brand = '暂无'

        content_list.append(model)
        content_list.append(brand)

        print(content_list)

        return content_list
    except:
        print('无法找到内容')

# 型号 ：model
# 运行内存：  running_memory
# 存储容量：  phone_memory
# 处理器：  cpu
# 屏幕尺寸：  screen_size
# 电池容量：  battery_life
# 品牌 ： brand

def find_flat(soup):
    try:
        #爬取价格
        content_list = []
        #tab_con = soup.find_all('div',{'class':'tab-con'})[3]
        #one_item = str(tab_con.find_all('div',{'class','Ptable'})[0])
        one_item = str(soup)
        rModel = '<dt>型号</dt><dd>(.+?)</dd>'
        try:
            model = re.findall(rModel,one_item)[0]
        except:
            try:
                rModel = '<li title=\'(.+?)\'>商品名称'
                model = re.findall(rModel, one_item)[0]
            except:
                model = '暂无'

        rRuning_memory = '<dt>运行内存</dt><dd>(.+?)</dd>'
        try:
            running_memory = re.findall(rRuning_memory,one_item)[0]
        except:
            running_memory = '暂无'

        rPhone_memory = '>存储容量：(.+?)</li>'
        try:
            phone_memory = re.findall(rPhone_memory,one_item)[0]
        except:
            phone_memory='暂无'

        rCpu = '<dt>处理器</dt><dd>(.+?)</dd>'
        try:
            cpu = re.findall(rCpu,one_item)[0]
        except:
            cpu='暂无'
        rScreen_size = '<dt>屏幕尺寸</dt><dd>(.+?)</dd>'
        try:
            screen_size = re.findall(rScreen_size,one_item)[0]
        except:
            screen_size='暂无'

        rBattery_life = '<dt>电池容量</dt><dd>(.+?)</dd>'
        try:
            battery_life = re.findall(rBattery_life, one_item)[0]
        except:
            battery_life = '暂无'

        rBrand = '<li title=\"(.+?)\">品牌： <a'
        try:
            brand = re.findall(rBrand, one_item)[0]
        except:
            brand = '暂无'

        content_list.append(model)
        content_list.append(running_memory)
        content_list.append(phone_memory)
        content_list.append(cpu)
        content_list.append(screen_size)
        content_list.append(battery_life)
        content_list.append(brand)
        print(content_list)

        return content_list
    except:
        print('无法找到内容')


def parser(html):
    try:
        soup = bs4.BeautifulSoup(html,'html.parser')
        return soup
    except:
        print('解析网页失败')

def Primary(url,goods_id):

    html = 'null'
    soup = 'null'
    list = 'null'
    content_list = 'null'

    html = open_url(url)
    if html != 'null':
        soup = parser(html)
    if soup != 'null':
        if goods_id[0:1] == '1':
            list = find_phone(soup)
            if list ==None:
                list=['null','null','null','null','null','null','null']
        if goods_id[0:1] == '2':
            list = find_computer(soup)
            if list ==None:
                list=['null','null','null','null','null','null','null']
        if goods_id[0:1] == '3':
            list = find_earphone(soup)
            if list ==None:
                list=['null','null']
        if goods_id[0:1] == '4':
            list = find_flat(soup)
            if list ==None:
                list=['null','null','null','null','null','null','null']

    dict[url] = list
    # else:
    #     content_list=['null','null','null']
    #     dict[url] = content_list
    # if html == 'null' or soup =='null' or list =='null' or content_list == 'null':
    #     print(url +'无法成功爬取')
    #     fail_list.append(url)

def store_database(dict):
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')
    if goods_id[0:1] == '1':
        for key in dict:
            cur.execute('update goods_detail set model= %s,cpu =%s,running_memory = %s ,phone_memory = %s ,screen_size = %s ,battery_cap = %s ,brand = %s where goods_url = %s',(dict[key][0],dict[key][1],dict[key][2],dict[key][3],dict[key][4],dict[key][5],dict[key][6],key))
    if goods_id[0:1] == '2':
        for key in dict:
            cur.execute('update goods_detail set model= %s,graphics_card =%s,cpu = %s ,running_memory = %s ,phone_memory = %s ,screen_size = %s ,brand = %s where goods_url = %s',(dict[key][0],dict[key][1],dict[key][2],dict[key][3],dict[key][4],dict[key][5],dict[key][6],key))
    if goods_id[0:1] == '3':
        for key in dict:
            cur.execute('update goods_detail set model= %s,brand = %s where goods_url = %s',(dict[key][0],dict[key][1],key))
    if goods_id[0:1] == '4':
        for key in dict:
            cur.execute('update goods_detail set model= %s,running_memory =%s,phone_memory = %s ,cpu = %s ,screen_size = %s ,battery_life = %s ,brand = %s where goods_url = %s',(dict[key][0],dict[key][1],dict[key][2],dict[key][3],dict[key][4],dict[key][5],dict[key][6],key))

    conn.commit()
    cur.close()
    conn.close()

dict={}
if __name__ == "__main__":
    num = 'null'
    # final_list =[]
    goods_id = '11%'
    #url = ['https://item.jd.com/34319348140.html','https://item.jd.com/34319505431.html','https://item.jd.com/63836956459.html']
    url = get_url(goods_id)
    num = len(url)
    if num != 'null':
        for i in range(len(url)):
            print("-------正在获取第{0}个商品的数据,一共{1}个-----------".format(i,num))
            Primary(url[i],goods_id)
            time.sleep(0.5)
    print(dict)

    store_database(dict)
    # else:
    #     print('从数据库中获取数据失败')