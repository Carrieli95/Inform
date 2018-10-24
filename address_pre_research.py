import re
from pro_utils.read_files import read_excel_files
from pro_utils.regex_finder import re_match_single
import copy


fake_data = {'PRUEBA'}
trans_pattern = {'CIUDAD': 'city', 'CANTON': 'city', 'CIUD': 'city', 'province': 'prov', 'PROVINCIA': 'prov', 'PROV': 'prov',
                 'DIR': 'address', 'DIRECCION': 'address', 'Dir': 'address', 'REF': 'reference'}
add_pattern = {'province': r'prov.*\n', 'sector': r'sector.*\n',
               'address': r'address.*\n', 'reference': r'reference.*\n', 'city': r'city.*\n'}
get_rid_of = {'prov', 'PROVINCE', ' / ', 'sector', 'address', 'reference', 'city',
              'PROV', 'SECTOR', 'ADDRESS', 'CITY', 'REFERENCE'}


def format_changer(string, format_dic):
    """
    change certain words in a text to a-desire-expression
    :param string: string that contains need-to-convert elements
    :param format_dic: dict stores target format
    :return: string after words replacement
    """
    if not isinstance(string, str):
        string = str(string)
    for key, ele in format_dic.items():
        string = string.replace(key, ele)
    return string


def extract_address_from_des(content):
    if isinstance(content, list):
        if len(content) == 0:
            return []
    elif content is None:
        return []
    extraction_list = []
    extraction = {}
    if isinstance(content, list):
        for ele in content:
            temp = format_changer(ele, trans_pattern)
            for key_1, ele_1 in add_pattern.items():
                extraction[key_1] = re_match_single(ele_1, temp).strip('\n')
                print(key_1, extraction[key_1])
                for a in get_rid_of:
                    extraction[key_1] = extraction[key_1].replace(a, '', re.IGNORECASE)
            if extraction['reference']:
                extraction['combine_address'] = extraction['address'] + '--' + extraction['reference']
            extraction_tp = copy.deepcopy(extraction)
            extraction_list.append(extraction_tp)

    return extraction_list


if __name__ == "__main__":
    read_data = read_excel_files('experiment_test.xlsx')
    event_description = read_data['TransLate'][0:5].tolist()
    print(event_description)
    result = extract_address_from_des(event_description)
    print(result)

