import pandas as pd
import os

par_path = "/Users/carrie/Documents/辰安信息/数据相关/报警电话翻译/urltxtFiles"


def read_excel_files(filename, read_path):
    path = os.path.join(read_path, filename)
    read_res = pd.read_excel(path)
    return read_res


def read_txt_files(par_path, filename):
    path = os.path.join(par_path, filename)
    res = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            each_line = line.strip()
            res.append(each_line)
    return res


def read_txt_files_as_whole(par_path, filename):
    path = os.path.join(par_path, filename)
    res = ''
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            each_line = line.strip()
            res = res+each_line
    return res


if __name__ == '__main__':
    # test = read_excel_files('test_test.xlsx')
    # print(test['TransLate'])
    test = read_txt_files_as_whole(par_path, '1_span.txt')
    print(test)

