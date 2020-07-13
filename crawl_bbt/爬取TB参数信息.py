import urllib.request
import bs4
import re
import requests
import pymysql
import time
import json
from urllib.request import urlretrieve

def get_url(goods_id):
    url=[]
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')  # GOODS_ID like %s', ('15%')
    cur.execute('select GOODS_ID,GOODS_URL from goods_detail where GOODS_ID like %s', (goods_id) )
    for i in cur:
        url.append(i[1])
    cur.close()
    conn.close()
    print(url)
    return url



def open_url(url):
    try:
        header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'accept-language':'zh-CN,zh;q=0.9',
                  'cookie':'hng=CN%7Czh-CN%7CCNY%7C156; cna=+ibIFv0D3nkCAXAOQrEc4DFn; lid=%E5%B0%8F%E5%88%B7a; enc=R9SD%2FaDPY4bbthKg%2BCGCQ967rdZnuC8KcOEgknYHOMdJGoldjJB5tQTbiSnwl8aGBjxj9fWqeQshnYcNqkTzwA%3D%3D; cq=ccp%3D1; _m_h5_tk=61e2baaa25c0979bc7b8d7c59d93f055_1581507530698; _m_h5_tk_enc=8cb319df07b4bd0eee69e4051821d8fe; t=78c747d81b73b6dc3cc7cd57820a35f5; _tb_token_=e3b9aa5e76d8; cookie2=14f244159b0f780e27225c13ad386b0c; pnm_cku822=098%23E1hvk9vUvbpvUpCkvvvvvjiPn2zZlj1En2FWgj3mPmPhljYRn2qZQjDEnL5wAjt8n2yCvvpvvhCvkphvC9hvpyPwt8yCvv9vvhh1GbBEvbyCvm9vvhCvvvvvvvvvByOvvUmjvvCVB9vv9LvvvhXVvvmCjvvvByOvvUhwmphvLUvP3IOa0fJ6W3CQog0HKfUpVcEUAXZTKFyzOvxrs8TJ%2BulsbuAUrqOBHkyZAnk4HFKz8Z0vQE01%2BbyDCwFWjLeARFxjKOmAdXkfjovCvpvVvvBvpvvv2QhvCvvvvvm5vpvhvvCCBv%3D%3D; l=cBgH5VHHQYkOoP5EKOCwourza77OSIRAguPzaNbMi_5QK6Y_vKQOo7KDpFv6VjWdtdTB4Tn8Nr29-etkm5vboA1P97RN.; isg=BM7OkIBfHH1z0qhfbkUi3SjbH6SQT5JJTaN0TfgXOlGMW261YN_iWXQZk4c3w4ph'}
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

###
# 产品名称：model
# CPU品牌：  cpu
# 运行内存RAM：  running_memory
# 存储容量：  phone_memory
# 屏幕尺寸：  screen_size
# 电池类型：  battery_cap
# 品牌 ： brand
def find_phone(soup):

    content_list=[]
    one_item = str(soup)
    try:
        rModel = '<tr><th>产品名称</th><td>(.+?)</td>'
        model = str(re.findall(rModel,one_item)[0]).replace("\xa0","")
    except:
        try:
            rModel = '<li title=\"(.+?)\">产品名称'
            model = str(re.findall(rModel,one_item)[1]).replace("\xa0","")
        except:
            model="暂无"
    try:
        rCpu = '<tr><th>CPU品牌</th><td>(.+?)</td>'
        cpu = str(re.findall(rCpu, one_item)[0]).replace("\xa0", "")
    except:
        cpu="暂无"

    try:
        rRunning_memory = '<tr><th>运行内存RAM</th><td>(.+?)</td>'
        running_memory = str(re.findall(rRunning_memory, one_item)[0]).replace("\xa0", "")
    except:
        running_memory="暂无"

    try:
        rPhone_memory = '<tr><th>存储容量</th><td>(.+?)</td>'
        phone_memory = str(re.findall(rPhone_memory, one_item)[0]).replace("\xa0", "_")
    except:
        phone_memory="暂无"

    try:
        rScreen_size = '<tr><th>屏幕尺寸</th><td>(.+?)</td>'
        screen_size = str(re.findall(rScreen_size, one_item)[0]).replace("\xa0", "")
    except:
        screen_size="暂无"

    try:
        rBattery_cap = '<tr><th>电池类型</th><td>(.+?)</td>'
        battery_cap = str(re.findall(rBattery_cap, one_item)[0]).replace("\xa0", "")
    except:
        battery_cap="暂无"

    try:
        rBrand = '<tr><th>品牌</th><td>(.+?)</td>'
        brand = str(re.findall(rBrand, one_item)[0]).replace("\xa0", "")
    except:
        brand="暂无"

    content_list.append(model)
    content_list.append(cpu)
    content_list.append(running_memory)
    content_list.append(phone_memory)
    content_list.append(screen_size)
    content_list.append(battery_cap)
    content_list.append(brand)
    print(content_list)
    return content_list


## 电脑属性类型
#   型号： model
#   显卡类型 graphics_card  内建GPU
#   CPU cpu
#   内存容量 running_memory
#   机械硬盘容量 phone_memory
#   屏幕尺寸 screen_size
#   品牌  brand
# #
def find_computer(soup):

    content_list=[]
    one_item = str(soup)
    try:
        rModel = '<li title=\"(.+?)\">型号'
        model = str(re.findall(rModel,one_item)[0]).replace("\xa0","")
    except:
        try:
            rModel = '<li title=\"(.+?)\">产品名称'
            model = str(re.findall(rModel, one_item)[1]).replace("\xa0", "")
        except:
            model="暂无"
    try:
        rGraphics_card = '<tr><th>显卡类型</th><td>(.+?)</td>'
        graphics_card = str(re.findall(rGraphics_card, one_item)[0]).replace("\xa0", "")
    except:
        try:
            rGraphics_card = '<li title=\"(.+?)\">显卡系列'
            graphics_card = str(re.findall(rGraphics_card, one_item)[0]).replace("\xa0", "")
        except:
            graphics_card="暂无"

    try:
        rCpu = '<tr><th>CPU</th><td>(.+?)</td>'
        cpu = str(re.findall(rCpu, one_item)[0]).replace("\xa0", "")
    except:
        try:
            rCpu = '<li title=\"(.+?)\">CPU系列'
            cpu = str(re.findall(rCpu, one_item)[0]).replace("\xa0", "")
        except:
            cpu = "暂无"
    try:
        rRunning_memory = '<tr><th>内存容量</th><td>(.+?)</td>'
        running_memory = str(re.findall(rRunning_memory, one_item)[0]).replace("\xa0", " ")
    except:
        try:
            rRunning_memory = '<li title=\"(.+?)\">内存容量'
            running_memory = str(re.findall(rRunning_memory, one_item)[0]).replace("\xa0", "")
        except:
            running_memory="暂无"
    try:
        rPhone_memory = '<tr><th>机械硬盘容量</th><td>(.+?)</td>'
        phone_memory = str(re.findall(rPhone_memory, one_item)[0]).replace("\xa0", "")
    except:
        try:
            rPhone_memory = '<li title=\"(.+?)\">硬盘容量'
            phone_memory = str(re.findall(rPhone_memory, one_item)[0]).replace("\xa0", "")
        except:
            phone_memory="暂无"

    try:
        rScreen_size = '<tr><th>屏幕尺寸</th><td>(.+?)</td>'
        screen_size = str(re.findall(rScreen_size, one_item)[0]).replace("\xa0", "")
    except:
        screen_size="暂无"

    try:
        rBrand = '<tr><th>品牌</th><td>(.+?)</td>'
        brand = str(re.findall(rBrand, one_item)[0]).replace("\xa0", "")
    except:
        try:
            rBrand = '<li id=\".+?\" title=\"(.+?)\">品牌:'
            brand = str(re.findall(rBrand, one_item)[0]).replace("\xa0", "")
        except:
            brand="暂无"

    content_list.append(model)
    content_list.append(graphics_card)
    content_list.append(cpu)
    content_list.append(running_memory)
    content_list.append(phone_memory)
    content_list.append(screen_size)
    content_list.append(brand)
    print(content_list)
    return content_list

# 型号：model
# 品牌：  brand
def find_earphone(soup):

    content_list=[]
    one_item = str(soup)
    try:
        rModel = '<li title=\"(.+?)\">型号'
        model = str(re.findall(rModel,one_item)[0]).replace("\xa0","")
    except:
        try:
            rModel = '<li title=\"(.+?)\">苹果耳机型号'
            model = str(re.findall(rModel, one_item)[0]).replace("\xa0", "")
        except:
            model="暂无"

    try:
        rBrand = 'li id=\".+?\" title=\"(.+?)\">品牌'
        brand = str(re.findall(rBrand, one_item)[0]).replace("\xa0", "")
    except:
        brand="暂无"

    content_list.append(model)
    content_list.append(brand)
    print(content_list)
    return content_list

# 型号 ：model
# 内存容量：  running_memory
# 存储容量：  phone_memory
# 处理器型号信息：  cpu
# 屏幕尺寸：  screen_size
# 网络类型：  battery_life
# 品牌 ： brand
def find_flat(soup):

    content_list=[]
    one_item = str(soup)

    try:
        rModel = '<li title=\"(.+?)\">型号'
        model = str(re.findall(rModel,one_item)[0]).replace("\xa0","")
    except:
        model = "暂无"

    try:
        rRunning_memory = '<li title=\"(.+?)\">内存容量'
        running_memory = str(re.findall(rRunning_memory, one_item)[0]).replace("\xa0", "")
    except:
        running_memory="暂无"

    try:
        rPhone_memory = '<li title=\"(.+?)\">存储容量'
        phone_memory = str(re.findall(rPhone_memory, one_item)[0]).replace("\xa0", "")
    except:
        phone_memory = "暂无"

    try:
        rCpu = '<tr><th>处理器型号信息</th><td>(.+?)</td>'
        cpu = str(re.findall(rCpu, one_item)[0]).replace("\xa0", " ")
    except:
        cpu = "暂无"

    try:
        rScreen_size = '<li title=\"(.+?)\">屏幕尺寸'
        screen_size = str(re.findall(rScreen_size, one_item)[0]).replace("\xa0", "")
    except:
        screen_size="暂无"

    try:
        rBattery_life = '<tr><th>网络类型</th><td>(.+?)</td>'
        battery_life = str(re.findall(rBattery_life, one_item)[0]).replace("\xa0", "")
    except:
        battery_life="暂无"

    try:
        rBrand = '<li id=\".+?\" title=\"(.+?)\">品牌'
        brand = str(re.findall(rBrand, one_item)[0]).replace("\xa0", "")
    except:
        brand = "暂无"

    content_list.append(model)
    content_list.append(running_memory)
    content_list.append(phone_memory)
    content_list.append(cpu)
    content_list.append(screen_size)
    content_list.append(battery_life)
    content_list.append(brand)
    print(content_list)
    return content_list

def store_database(dict):
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')
    if goods_id[0:1] == '6':
        for key in dict:
            print("正在存储url为："+key)
            cur.execute('update goods_detail set model= %s,cpu =%s,running_memory = %s ,phone_memory = %s ,screen_size = %s ,battery_cap = %s ,brand = %s where goods_url = %s',(dict[key][0],dict[key][1],dict[key][2],dict[key][3],dict[key][4],dict[key][5],dict[key][6],key))
    if goods_id[0:1] == '7':
        for key in dict:
            print("正在存储url为：" + key)
            cur.execute('update goods_detail set model= %s,graphics_card =%s,cpu = %s ,running_memory = %s ,phone_memory = %s ,screen_size = %s ,brand = %s where goods_url = %s',(dict[key][0],dict[key][1],dict[key][2],dict[key][3],dict[key][4],dict[key][5],dict[key][6],key))
    if goods_id[0:1] == '8':
        for key in dict:
            print("正在存储url为：" + key)
            cur.execute('update goods_detail set model= %s,brand = %s where goods_url = %s',(dict[key][0],dict[key][1],key))
    if goods_id[0:1] == '9':
        for key in dict:
            print("正在存储url为：" + key)
            cur.execute('update goods_detail set model= %s,running_memory =%s,phone_memory = %s ,cpu = %s ,screen_size = %s ,battery_life = %s ,brand = %s where goods_url = %s',(dict[key][0],dict[key][1],dict[key][2],dict[key][3],dict[key][4],dict[key][5],dict[key][6],key))

    conn.commit()
    cur.close()
    conn.close()


dict = {}
fail_list = []
def Primary(url,goods_id):
    html = 'null'
    soup = 'null'
    list = 'null'
    content_list = 'null'

    html = open_url(url)
    if html != 'null':
        soup = parser(html)
    else:
        return
    if soup != 'null':
        if goods_id[0:1] == '6':
            list = find_phone(soup)
            if list ==None:
                list=['null','null','null','null','null','null','null']
        if goods_id[0:1] == '7':
            list = find_computer(soup)
            if list ==None:
                list=['null','null','null','null','null','null','null']
        if goods_id[0:1] == '8':
            list = find_earphone(soup)
            if list ==None:
                list=['null','null']
        if goods_id[0:1] == '9':
            list = find_flat(soup)
            if list ==None:
                list=['null','null','null','null','null','null','null']
        dict[url] = list


    # if html == 'null' or soup =='null' or list =='null' or content_list == 'null':
    #     print(url +'无法成功爬取')
    #     fail_list.append(url)



if __name__ == "__main__":
    num = 'null'
    goods_id = '96%'
    url = get_url(goods_id)
    #url = ['https://detail.tmall.com/item.htm?id=596577969318','https://detail.tmall.com/item.htm?id=597142202458']
    #dict_url ={61002: 'https://detail.tmall.com/item.htm?id=609asasasa'}
    #dict_url = get_url()
    num = len(url)
    if num != 'null':
        for i in range(len(url)):
            print("-------正在获取第{0}个商品的数据,一共{1}个-----------".format(i, num))
            Primary(url[i], goods_id)
            time.sleep(0.5)
    print(dict)

    store_database(dict)
    # else:
    #     print('从数据库中获取数据失败')



