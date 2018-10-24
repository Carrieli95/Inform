# -*- coding: utf-8 -*-
from urllib.request import urlopen
import re
import pandas as pd


def read_from_url(filename):
    """
    如果是csv或excel文件，返回pandas DataFrame类型
    如果是txt文件，返回list型
    如果非以上三种，返回空[]list
    :param filename: 传入想要读取的文件名
    :return:
    """
    try:
        host = "http://192.168.89.232:8000/urltxtFiles/"
        host = host + filename
        excel_pattern = r'.xls[x]?'
        txt_pattern = r'.txt'
        csv_pattern = r'.csv'
        excel_file = re.findall(excel_pattern, filename)
        txt_file = re.findall(txt_pattern, filename)
        csv_file = re.findall(csv_pattern, filename)
        if excel_file:
            response = urlopen(host)
            file = pd.read_excel(response, engine='xlrd')
            return file
        elif txt_file:
            response = urlopen(host).read().decode("utf-8")
            file = response.split("\n")
            return file
        elif csv_file:
            response = urlopen(host)
            file = pd.read_csv(response, sep=',')
            return file
        else:
            return []
    except Exception as e:
        print("Error from read_excel_from_url " + str(e))


if __name__ == "__main__":
    pass
