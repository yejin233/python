# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 23:46:01 2022

@author: admin
"""

import requests
import tqdm
import parsel
import re
import prettytable as pt

import time
import threading
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor


def get_response(html_url):
  
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    #proxies = {'https':'https://124.70.94.247:3128'}挂代理 但是没有好用的代理
    s.keep_alive = False#关闭多余的连接
    head = {# 模拟头部信息
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response=requests.get(url=html_url,headers=head)
    
    return response
def get_content(name,html_url):    
    response=get_response(html_url)
    selector=parsel.Selector(response.text)
    title=selector.css("#read > div.book.reader > div.content > h1::text").get()
    content_list=selector.css("#chaptercontent::text").getall()#这里有点奇怪，因为源代码中以br分割了整个小说内容，本来应该能用get直接爬取，但是用get只能爬取一个br，后面的爬取不到，而且如果采用爬取br内容，要么爬不到要么爬的都是br
    #content_list=selector.css("#chaptercontent::text").get()
    #content_list=selector.css("#chaptercontent>br::text").getall()
    content='\n'.join(content_list)
    #print(content_list)
    #print(title)
    #print(content)
    with open(name+".txt",mode='a',encoding="utf-8") as f:
        f.write(title)
        f.write('\n')
        f.write(content)
        f.write('\n')

def get_list_url(html_url):
    response=get_response(html_url)
    list_url=re.findall('<dd><a href ="(.*?)">.*?</a></dd>',response.text)
    # selector=parsel.Selector(response.text)
    # list=selector.css("body > div.listmain > dl > dd > a::text").getall()
    #该网站中途做了一个展开处理，故不可以采用直接分析的方法，要选用正则表达式
    #print(list_url)
    return list_url

def main(html_url):
    list_url=get_list_url(html_url) 
    html_data=get_response(html_url).text
    name=re.findall('<dt>(.*?)最新章节列表</dt>',html_data)
    #print(name)
    #print(list_url)
    with ThreadPoolExecutor(50) as pool:
        for link in tqdm.tqdm(list_url):
            link_url="https://www.bige3.com"+link
            sub=pool.submit(get_content,''.join(name),link_url)
            print(sub.result())
    #         def get_result(future):
    #             print(threading.current_thread().name + '运行结果：' + str(future.result()))
 
 
    # # 查看future1代表的任务返回的结果
        #sub.add_done_callback(get_result)
            #print(sub.result())#不打印这个直接寄
       # futures={}
    # for link in tqdm.tqdm(list_url):
    #     link_url="https://www.bige3.com"+link
            
    #     #     sub=pool.submit(get_content,''.join(name),link_url)
    #         #data=[''.join(name),link_url]
            
    #         #futures[sub]=link_url
    #     get_content(''.join(name),link_url)
def 搜索():
    while True:
        keyword=input("搜索书名 输入exit退出")
        if keyword=="exit":
            break
        # url="https://www.bige3.com/book/2749/"
        # main(url)
        # urll="https://www.bige3.com/s?q="
        search_url=f'https://www.bige3.com/s?q={keyword}'#查找输入网站//爬搜索栏
        html_data=get_response(search_url).text
        selectors=parsel.Selector(html_data)
        book_list=selectors.css(".bookbox")
        num=0
        tb=pt.PrettyTable()
        tb.field_names=["序号","书名","作者","书id"]
        lis=[]
        for index in book_list:
            name=index.css('.bookname a::text').get()
            href=index.css('.bookname a::attr(href)').get().split('/')[-2]
            author=index.css('.author::text').get().replace('作者,','')
            #print(name,href,author)
            dit={"姓名":name,
                  "作者":author,
                  "书id":href
                }
            lis.append(dit)
            tb.add_row([num,name,author,href])
            num+=1
        print(tb)
        word=input("序号为")
        novel_id=lis[int(word)]["书id"]
        url=f'http://www.bige3.com/book/{novel_id}'
        main(url)
if __name__=='__main__':
    搜索()
  
        
        
             
        
        
            
        
        
    
    