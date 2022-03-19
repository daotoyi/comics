'''
Author: your name
Date: 2021-07-02 21:59:42
LastEditTime: 2021-09-02 15:05:09
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Python\picture\picsdl.py
'''

import os
import time
import json
import random
import requests
import threading 
import logging
from lxml import etree
from contextlib import closing
import string

import sys
sys.path.append(r"E:\Refine\Python")
from custom.agent import Agent
from custom import useragent

logging.basicConfig(level=logging.INFO,format='[%(asctime)s] %(filename)s [line:%(lineno)d] \
[%(levelname)s]  %(message)s',  datefmt='%Y-%m-%d(%a) %H:%M:%S')


class Comics():
    '''Comics pics from WEB'''

    def __init__(
        self, 
        multithread: int=None,
        server: str='https://www.szcdmj.com', 
        target: str='', 
        headers: dict={'User-Agent': random.choice(Agent.HEADERS)},
        save_path: str=''
    ) -> None:
        self.multithread = multithread
        self.server = server
        self.target = target
        self.headers = headers
        self.save_path = os.path.join(os.getcwd(), save_path)

        logging.debug(self.headers)
        ua_header = {'User-Agent': useragent.get_user_agent(browser='chrome')}
        logging.debug(ua_header)
        
        self.lock = threading.RLock()
    
    def start(self) -> None:
        ''''''
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            print("==> Target Directory Created.")
        else:
            print("==> Target Directory Exist.")

        chapter_name, chapter_url = self.get_all_urls()
        if self.multithread != 0:
            self.multithread_down(chapter_name, chapter_url)
        else:
            self.down(chapter_name, chapter_url)

    def get_all_urls(self) -> list:
        '''return chapter_name and chapter_url list'''
        response = requests.get(self.target, headers = self.headers, timeout=3)
        response.encoding = "utf-8"
        logging.debug(response.status_code)
        html = etree.HTML(response.text)
        html_chapter_url = html.xpath('//div[@id="chapterlistload"]/ul/li/a/@href')
        chapter_name = html.xpath('//div[@id="chapterlistload"]/ul/li/a/text()')
        logging.debug(chapter_name)

        chapter_url = []
        for each in html_chapter_url: 
            # #delete '/' first character in str,but add '\' (on window)uncongnize in broswer.
            # url = os.path.join(self.server, each[1:])
            url = self.server + each
            chapter_url.append(url)
        logging.debug(chapter_url)
        
        return chapter_name, chapter_url

    def multithread_down(self, names: list, urls: list) -> None:
        ''''''
        serial = [n for n in range(len(names))]
        logging.debug(serial)

        zip_obj = zip(names, urls, serial)
        name_url = list(zip_obj)
        name_url.reverse()

        def down():
            while len(name_url) > 0:
                self.lock.acquire()
                obj = name_url.pop() # pop from the last index.
                self.lock.release()
                self.down_chapter(name=obj[0], url=obj[1], chapter_num=obj[2])
                logging.debug(obj[0], obj[1])

        for _ in range(self.multithread):
                thread = threading.Thread(target=down)
                print(f'- {thread.getName()} <{thread.ident}> start.')
                thread.start()
 
    def down(self, names:list, urls:list) -> None:
        num = 0
        for name, url in zip(names, urls):
            num += 1
            self.down_chapter(name, url, num)

    def down_chapter(self, name:str, url:str, chapter_num:int) -> None:
        ''''''
        response = requests.get(url, headers = self.headers, timeout=3)
        response.encoding = "utf-8"
        html = etree.HTML(response.text)
        urls = html.xpath('//div/img[@class="lazy"]/@data-original')
        # urls = html.xpath('//div/img[@class="lazy"]/@src')
        logging.debug(urls)
        # self.save_chapter(name, urls, chapter_num)
        self.save_onedir(name, urls, chapter_num)
                    
    def save_chapter(self, dirname: str, urls:list, sectionNum: int) -> None:
        ''''''
        # delete punctuation(en_US), or os.makeidrs raise error.
        for i in string.punctuation:
            dirname = dirname.replace(i, '')
        
        if not os.path.exists(self.save_path+'\\'+dirname):
            os.makedirs(self.save_path + dirname)
            num = 0
            for url in urls:
                num += 1
                filename = str(num) +'.jpg'
                try:
                    r = requests.get(url,headers=self.headers)
                    with open(self.save_path + dirname + '\\' + filename ,'wb') as f :
                        f.write(r.content)
                        f.flush()
                        # f.close
                    print("\r==> chapter %d - %d download..." % (len(urls), num), end = '')
                except Exception as e:
                    # raise
                    continue
            print("\n==> Chapter:%d Saved! <==\n" % sectionNum)
        else:
            logging.info(f'exist - {dirname}')

    def save_onedir(self, dirname: str, urls:list, sectionNum: int):

        num = 0
        for url in urls:
            num += 1
            filename = f'chapter{sectionNum}-{str(num)}' +'.jpg'
            try:
                r = requests.get(url,headers=self.headers)
                with open(self.save_path + '\\' + filename ,'wb') as f :
                    f.write(r.content)
                    f.flush()
                    # f.close
                print("==> chapter %d - %d download..." % (sectionNum, num))
            except Exception as e:
                continue
        print("\n==> Chapter:%d Saved! <==\n" % sectionNum)


class Unsplash():
    ''''''
    #todo need to verify this class.
    
    def __init__(self):
        self.server = 'https://unsplash.com/'
        self.target = 'https://unsplash.com/s/photos/sky'
        self.headers = {'authorization':'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626'}
        # self.headers = {'User-Agent': random.choice(Agent.HEADERS)}
        self.photos_id = []
    
    def start(self):
        self.get_urls()
        for i in range(len(self.photos_id)):
            print('download %d image...' % (i+1))
            self.download(self.photos_id[i], (i+1))
        
    def get_urls(self):
        req = requests.get(url=self.target, headers=self.headers, verify=False)
        html = json.loads(req.text)
        next_page = html['next_page']
        for each in html['photos']:
            self.photos_id.append(each['id'])
        time.sleep(1)
        for i in range(5):
            req = requests.get(url=next_page, headers=self.headers, verify=False)
            html = json.loads(req.text)
            next_page = html['next_page']
            for each in html['photos']:
                self.photos_id.append(each['id'])
            time.sleep(1)

    def download(self, photo_id, filename):
        target = self.server.replace('xxx', photo_id)
        with closing(requests.get(url=target, stream=True, verify=False, headers=self.headers)) as r:
            with open('%d.jpg' % filename, 'ab+') as f:
               for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()