# -*- coding:utf-8 -*-
'''
Author: your name
Date: 2021-07-02 21:34:39
LastEditTime: 2022-03-19 20:38:04
LastEditors: daoyi
Description: In User Settings Edit
FilePath: \Python\picture\comicsdown.py
'''
import sys
# sys.path.append("E:\Refine\Python")

from picsdl import Comics

def yi_ren_zhi_xia():
    server = "https://www.szcdmj.com"
    target = "https://www.szcdmj.com/szcbook/3234"
    save_path = "E:\\Recreation\\Comics\\yiRenZhiXia\\"

    p = Comics(multithread=10, server=server, target=target, save_path=save_path)
    p.start()

def quan_zhi_fa_shi():
    # server = 'http://www.kuman57.com/'
    # target = 'http://www.kuman57.com/mulu/9845/1-1.html'
    server = "https://www.szcdmj.com" 
    target = 'https://www.szcdmj.com/szcbook/3350'
    save_path = "E:\\Recreation\\Comicst\\quanZhiFaShi\\"

    p = Comics(multithread=10, server=server, target=target, save_path=save_path)
    p.start()

if __name__ == "__main__":
    yi_ren_zhi_xia()
    # quan_zhi_fa_shi()