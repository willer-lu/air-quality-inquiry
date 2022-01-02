from tkinter import *
from tkinter import messagebox
import re
import requests
import pypinyin
import datetime

root = Tk()

def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


def get_weather_data(city_name):  # 获取网站数据
    piny = pinyin(city_name)# 获取输入框的内容
    url = 'http://www.tianqihoubao.com/aqi/{0}.html'.format(piny)
    response = requests.get(url).content.decode("gbk")
    res1 = r'<li>(.*?)</li>'
    res2 = r'<li>(.*?)<sup>3</sup></li>'
    res3 = r'<div class="num">([\s\S]*) <div class="status">'
    aqi = re.findall(res3, response)
    if aqi:
        s = aqi[0]
    else:
        print(messagebox.askokcancel("sorry", "你输入的城市名有误，或者该网站未收录你所在城市"))
        exit(0)
    L = [i for i in s if i != ' ' and i != '\n' and i != '\r']
    AQI = ''.join(L).split('<')[0]
    pAQI = 'AQI = ' + str(AQI)
    #print('AQI = ', AQI)
    list1 = re.findall(res1, response)
    list2 = re.findall(res2, response)  # 获取空气质量
    PM25 = list1[8]
    CO = list1[9]
    O3 = list1[12]
    SO2 = list2[0]
    PM10 = list2[1]
    NO2 = list2[2]   #获取对应的数据
    data1 = (pAQI,PM25, CO, O3, SO2, PM10, NO2)
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    return data1

def getcity():
    city_name = enter.get()
    data1 =get_weather_data(city_name)
    i = 1
    for data in data1:
        Label(root, text=data).grid(row=i+3, column=0)  # 设置标签并调整位置
        i = i+1

root.title('天气查询')  # 窗口标题
root.geometry("400x300")  # 设置窗口大小
Label(root, text='请输入城市').grid(row=0, column=0)  # 设置标签并调整位置
enter = Entry(root)  # 输入框
enter.grid(row=0, column=1, padx=20, pady=20)  # 调整位置
enter.delete(0, END)  # 清空输入框
Button(root, text="确认", width=10, command=getcity) \
                 .grid(row=3, column=0, sticky=W, padx=10, pady=5)
Button(root, text='退出', width=10, command=root.quit) \
             .grid(row=3, column=1, sticky=E, padx=10, pady=5)


root.mainloop()





