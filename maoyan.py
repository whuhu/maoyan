import requests
import re
import json
import time

def page(url):
    '''使用response函数抓取网页内容'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
    }#模拟firefox 4.0.1 浏览器访问网页
    response = requests.get(url, headers=headers)
    return response.text


def next_page(html):
    '''使用正则表达式作为解析工具'''
    #创建正则表达式对象，优化代码
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
        + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
        + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    contents = re.findall(pattern, html)
    for content in contents:
        yield {
            'index': content[0],
            'image': content[1],
            'title': content[2],
            'actor': content[3].strip()[3:],
            'time': content[4].strip()[5:],
            'score': content[5] + content[6]
        }


def to_file(content):
    '''写入文件'''
    with open('maoyan.txt', 'a', encoding='utf-8') as f:
        #使用JSON库的dumps方法实现字典的序列化，ensure_ascii为False以输出中文
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    #爬取前100(10面)的网页
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = page(url)
    for content in next_page(html):
        print(content)
        to_file(content)


if __name__ == '__main__':
    for i in range(10):
        #实现翻页
        main(offset=i * 10)
        time.sleep(1)
