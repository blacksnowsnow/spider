#!/usr/bin/env python
#__Author__:Elson Zeng
#_*_coding:utf-8_*_

import requests,re,bs4

#http://desk.zol.com.cn/1920x1080/
#http://xiazai.zol.com.cn/search?wd=%B7%E7%BE%B0&type=5&subid=8
#http://desk.zol.com.cn/bizhi/1282_15723_2.html
#http://desk.zol.com.cn/showpic/1920x1080_15723_102.html
#/bizhi/1282_15732_2.html

#http://desk.zol.com.cn/showpic/1920x1080_15732_102.html
#http://desk.zol.com.cn/showpic/1920x1080_15723_2.html
#/bizhi/1282_15723_2.html


header={
"Referer":"http://top.zol.com.cn/",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}
word = input("请输入要搜索的关键字：")

zol_url = "http://xiazai.zol.com.cn/search?wd={}&type=5&subid=8".format(word)

fir_text = requests.get(zol_url,headers=header).text
if re.findall(r'抱歉，没有找到与',fir_text):
    print("抱歉，没有找到与" + word + "相关内容！")
    exit()
#<a target="_blank" href="http://desk.zol.com.cn/bizhi/1292_15848_2.html"><img alt
img_num = int(input("请输入要下载的图片数量："))
url_sec = re.findall('<a target="_blank" href="(http://desk.zol.com.cn/bizhi/\d+_\d+_2.html)"><',fir_text,re.S)
#print(url_sec)

img_urls = []
num = 0
#<a href="/bizhi/1282_15723_2.html">
for sec_text in list(set(url_sec)):
    #print(2)
    thi_text = requests.get(sec_text,headers=header).text
    url_thi = re.findall('<a href="/bizhi/\d+(_\d+_2.html)">',thi_text)
    for img_text in url_thi:
        fou_url = "http://desk.zol.com.cn/showpic/1920x1080" + img_text
        fou_text = requests.get(fou_url,headers=header).text
        img_url = re.findall('<img src="(https://desk-fd.zol-img.com.cn\S+.jpg)">',fou_text)
        #print(1)
        for url in img_url:
            if num < img_num:
                #print (num)
                img_urls.append(url)
                num += 1
            else:
                break


a = 1

for down in img_urls:
    name = word + str(a) + ".jpg"
    img_path="C:\\Users\\asus\\Desktop\\work\\" + name
    #print(requests.get(down, headers=header).content)
    img_wb = requests.get(down, headers=header).content
    with open (img_path,"wb") as f:
        f.write(img_wb)
        print(img_path + "下载成功")
    a += 1

