#!/usr/bin/env python
#__Author__:Elson Zeng
#_*_coding:utf-8_*_

import requests,os,re,winreg

"""请求头，不然会被百度屏蔽"""
headers = {
    'Referer': 'https://image.baidu.com/search/index?tn=baiduimage',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}


def get_desktop():
    """获取桌面路径 ，get_desktop()) + '/' + file_name + '/' """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')#利用系统的链表
    return winreg.QueryValueEx(key, "Desktop")[0] #返回的是Unicode类型数据

#"thumbURL":"http://img5.imgtn.bdimg.com/it/u=1726186288,1673049835&fm=26&gp=0.jpg"

def get_picurl(work,num):
    """
    :param work: 下载名称
    :param num: 需要下载的数量
    :return:获取图片二进制
    """
    a = 0
    pic_wb = []
    for i in range(1,1000):
        url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=aa&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30&gsm=&1572592529769='.format(work, i * 30)
        baidu_url = requests.get(url,headers=headers).text
        pic_urls = re.findall('"thumbURL":"(.*?)"',baidu_url,re.S)
        for pic_url in pic_urls:
            #print(requests.get(pic_url,headers=headers))
            if requests.get(pic_url,headers=headers).status_code == 200:
                if a < int(num):
                    pic_wb.append(requests.get(pic_url,headers=headers).content)
                    a += 1
                else:
                    return pic_wb

def pic_download(file_path,down_wb):
    """
    :param file_path:保存的文件路径
    :param down_wb: 图片二进制
    :return: 保存图片
    """
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(down_wb)

def main():
    name_num = 1
    work = input('请输入需要爬取的数据：')
    pic_num = input('请输入需要下载的图片数量：')
    local_path = get_desktop() + '/' + work + '/'
    if not os.path.exists(local_path):
        os.mkdir(local_path)
    for down_wb in get_picurl(work,pic_num):
        file_path = local_path + work + '_%d.jpg' % name_num
        pic_download(file_path,down_wb)
        print( file_path + '下载成功' )
        name_num += 1


if __name__ == '__main__':
    main()
