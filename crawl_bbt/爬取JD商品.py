import urllib.request
import bs4
import time
import pymysql
from urllib.request import urlretrieve
#爬虫获取京东网站的除拍拍网商品的商品链接与商品描述 并存入数据库

def open_url(url):
    try:
        header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'accept-language':'zh-CN,zh;q=0.9'}
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
        all_content = soup.find_all('ul',{'class':'gl-warp clearfix'})[0]
        alone_net = all_content.find_all('li',{'class':'gl-item'})
        new_net = []
        for i in range(len(alone_net)):
            worry = alone_net[i].find('span',{'class':'p-tag'})
            if worry is None:
                new_net.append(alone_net[i])
            if worry is not None:
                text = worry.get_text()
                if text != '拍拍':
                    # print(alone_net[i])
                    new_net.append(alone_net[i])
        result = {}
        for i in range(len(new_net)):
            tmp_url = new_net[i].find('div',{'class':'p-img'}).find('a')['href']
            tmp_url = tmp_url.lstrip('https:')
            tem_img = new_net[i].find('div',{'class':'p-img'}).find('img',{'class':'err-product'}).get('source-data-lazy-img')
            img = 'http:'+tem_img
            # result.append(tmp_url)
            url_content = new_net[i].find_all('em')[1].get_text()
            result['https:'+tmp_url] = [url_content,img]

        return result
    except:
        print('获取数据失败')
#存入数据库
def store_database(final):
    conn = pymysql.connect(host='120.92.164.236', port=3306, user='tbb', password='bbttbb139', db='bbt')
    cur = conn.cursor()
    cur.execute('use bbt')
    cur.execute('select max(GOODS_ID) from goods_detail where GOODS_ID like %s', ('46%'))
    data = cur.fetchall()
    if str(data[0][0]) == 'None':
        num = 46001
    else :
        num = int(data[0][0])
    for one_list in final:
        for key in one_list:
            #开始存储
            cur.execute('select * from goods_detail where goods_url = %s ', (key))
            data = cur.fetchall()
            if data == ():
                num = num + 1
                img_name = 'D:\pycharm\imgs/searchImg' + str(num) + '.jpg'
                store_name='E:\search_img/searchImg' + str(num) + '.jpg'
                cur.execute('insert into goods_detail(GOODS_ID,GOODS_URL,GOODS_TITLE,SEARCH_IMG) values(%s,%s,%s,%s)',(num,key,one_list[key][0],store_name))
                urlretrieve(one_list[key][1], img_name)


    conn.commit()
    cur.close()
    conn.close()
    print('-----恭喜！已经成功存储--------')

def Primary(url):
    html = 'null'
    soup = 'null'
    result = 'null'

    try:
        html = open_url(url)
        if html != 'null':
            soup = parser(html)
        if soup != 'null':
            result = find_net(soup)

        print(result)
        return result
    except:
        print(url+'无法成功爬取')



if __name__ == "__main__":
    final = []  #存入所有爬到的数据的列表
    # url = 'https://search.jd.com/Search?keyword=https://search.jd.com/Search?keyword=%E6%91%86%E6%B8%A1%E8%80%85%E5%B9%B3%E6%9D%BF&enc=utf-8&wq=%E6%91%86%E6%B8%A1%E8%80%85%E5%B9%B3%E6%9D%BF&pvid=01f0c199b3934cf9939749dc140b6beb
    # 爬取前n页的网址和名字
    #url获取到后需要改两个地方 把page和s改成page={0}和s=  放入url 输入需要爬取的页数就可以使用
    for i in range(1,4):
        url = 'https://search.jd.com/Search?keyword=%E6%91%86%E6%B8%A1%E8%80%85%E5%B9%B3%E6%9D%BF&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=pingg%E8%80%B3%E6%9C%BA&page={0}&s=1&click=0'.format(2*i-1)
        print('------------------正在爬取第{0}页的链接与数据----------------'.format(i))
        result = Primary(url)
        if result == None:
            continue
        final.append(result)
        time.sleep(0.5)
    print(final)
    print('-------------------数据获取完成，开始存入数据库-------------------------')
    #存入数据库
    store_database(final)
