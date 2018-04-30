# coding:utf-8
# 整个代码基本思路：爬取http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000页面数据
# 然后扔到创建的csv文件里面作为下一步的数据源。通过研究http://bj.58.com/pinpaigongyu/pn/{page}
# /?minprice=2000_4000这个页面，我们可以很容易发现，在页面中，每条数据都是一个li标签。

from bs4 import BeautifulSoup
# 该库能够解析HTML和XML
from  urllib.parse import urljoin
# 拼接URL
import requests
# requests是python的一个HTTP客户端库，跟urllib类似。那为什么要用requests而不用urllib.request呢？官方文档中是这样说明的：
# python的标准库urllib.request提供了大部分需要的HTTP功能，但是API太逆天了，一个简单的功能就需要一大堆代码。
import csv
# csv模块，用来操作csv文件
# csv一般用作表格文件，直接用文本编辑器打开也可读，行与行之间用换行来隔开，列与列之间用逗号（也可）

# 西安url = "http://xa.58.com/pinpaigongyu/?from=58_pc_zf_list_ppgy_tab_ppgy&PGTID=0d3090a7-001e-3ec9-2bc4-a6d4d7a0bfa8&ClickID=2"
url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"

page = 0
# 已完成的页数序号，初始值为0

csv_file = open('rent.csv','w')
# 打开rent.csv文件，w表示以只写方式打开指定文件夹
csv_writer = csv.writer(csv_file,delimiter = ',')
#创建writer对象，指定文件与分隔符

while True:
    page += 1
    print("fetch:",url.format(page = page))
    # format函数的参数是一个JSON对象，返回一个组装好的url地址
    response = requests.get(url.format(page = page))
    # 通过GET访问页面fetch，使用request向服务器请求网页，获得完整的HTTP response
    # 抓取目标页面
    html = BeautifulSoup(response.text,"html.parser")
    # 创建一个BeautifulSoup对象
    # response.text获取页面正文
    # beautifulsoup把html结构化成对象，通过对象的方式取html内部元素
    # BeautifulSoup对象表示的是文档的全部内容
    house_list = html.select(".list > li")
    # 获取class = list的元素下所有的li元素
    # 类名选择器，标签选择器
    # 通过select()直接传入CSS选择器就可以完成选择


    ## 循环中读不到新的房源时结束
    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string
        # 得到标签包裹着的文本
        house_url = urljoin(url,house.select("a")[0]["href"])
        # house.select("a")[0]["href"]可以得到标签内属性的值
        # 由于此处读取到的链接路径是相对路径，所以需要urljoin得到完整的url地址
        house_info_list = house_title.split()
        # split()通过指定分隔符对字符串进行切片
        # 当前分隔符为默认分隔符，即所有的空字符均为分隔符，包括空格、换行、制表符等

        ## 如果第二列是公寓名则取第一列作为地址
        if "公寓" in house_info_list[1] or "青年社团" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]

        house_money = house.select(".money")[0].select("b")[0].string
        csv_writer.writerow([house_title,house_location,house_money,house_url])
        # 写一行数据


csv_file.close()
# 关闭文件



