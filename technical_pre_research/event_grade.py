# from pro_utils.read_files import read_excel_files
from configparser import ConfigParser
import pandas as pd
import os

cfg = ConfigParser()
cfg.read('address.ini')
excel_path = cfg.get('document_path', 'excel_path')

path = os.path.join(excel_path, 'Categories&Grades.xlsx')
category_table = pd.ExcelFile(path)

# type_table = category_table.parse('IncidentTypeDic')
# type_id = type_table['IncidentTypeId']
# parent_id = type_table['ParentId']
# type_dic = {}
# for ele in parent_id:
#     if ele >= 0:
#         type_dic[ele] = set()
#     else:
#         pass
# for key, ele in enumerate(parent_id):
#     if ele >= 0:
#         type_dic[ele].add(type_id[key])
#     else:
#         pass
# print(type_dic)

type_table = category_table.parse('IncidentGradeDic')
name = type_table['IncidentGradeName']
gd_id = type_table['IncidentGradeId']
grade = {}
for key, ele in enumerate(gd_id):
    if ele >= 0:
        grade[name[key]] = ele
    else:
        pass
print(grade)

