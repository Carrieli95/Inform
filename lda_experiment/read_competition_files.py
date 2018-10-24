import pandas as pd
import os
from pro_utils.regex_finder import re_match_single

uincode_set = {"\u2014", "\u201d", "\u2019", "\u2013", "\u201c"}
match_pattern = r'{.*}'
key_pattern = {'content': r'{"content":.*"id"', "id": r'"id": \d+', "title": r'"title":.*}'}
replace_pattern = {'{"content": ', '"id": ', ', "id"', '"title": ', "}"}


def read_context_from_test(filename):
    try:
        path = os.path.join(os.path.abspath('.'), filename)
        data_read = []
        with open(path, "r") as fp:
            for line in fp:
                data_read.append(line.strip())
        return data_read
    except Exception as e:
        print('Error from read_competition_files' + str(e))


def pre_processing(data_content):
    try:
        data_list = []
        for i in data_content:
            data_pre = {}
            data_temp = re_match_single(match_pattern, i)
            for key, ele in key_pattern.items():
                data_pre[key] = re_match_single(ele, data_temp)
                for mem in replace_pattern:
                    data_pre[key] = data_pre[key].replace(mem, '')
            data_list.append(data_pre)
        return data_list
    except Exception as e:
        print('Error from pre_processing' + str(e))


if __name__ == "__main__":
    data = read_context_from_test('context_train_test_0.txt')
    result = pre_processing(data)
    print(result)