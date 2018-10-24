from pro_utils.read_files import read_excel_files
from configparser import ConfigParser
import os
import re

filename = 'Repeat_event.xlsx'
invalid = {'hkjkkj', '1241241', '124124', 'test1', 'test2', 'test15', 'test13', '23123', '12321','sfdfdsfd',
              'ddfdfd', 'sddhjdh', 'aaaaaaaaaaaaaaa', 'ghhhhh', 'gfdgdgdggdgd', 'test11', '123123',
              'asdasd', 'sdfdf', '1231231'}

cfg = ConfigParser()
cfg.read('address.ini')
excel_path = cfg.get('document_path', 'excel_path')
model_dir = cfg.get('document_path', 'model_dir')


def count_duplicaiton(file, path, column):
    content_sheet = read_excel_files(file, path)
    target_column = content_sheet[column]
    count = 0
    test_count = 0
    for i in range(0, len(target_column)-1):
        j = i+1
        if target_column[i] == target_column[j]:
            count +=1
        else:
            pass
        if isinstance(target_column[i], float):
            pass
        elif 'PRUEBA' in target_column[i]:
            test_count += 1
        # if re.search(r'prueba', target_column[i]) !='':
        #     print(target_column[i])
        #     test_count += 1
    return count, test_count


if __name__ == "__main__":
    duplicate_num = count_duplicaiton(filename, excel_path, 'IncidentDescription')
    print(duplicate_num)