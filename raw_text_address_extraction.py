# from server_request_file import read_from_url
from configparser import ConfigParser
from pro_utils.read_files import read_txt_files

cfg = ConfigParser()
cfg.read('address.ini')
street_key = cfg.get('street', 'street')
district_key = cfg.get('district', 'district')
detail_loc_key = cfg.get('detail_loc', 'detail_loc')
nearby_loc_key = cfg.get('nearby', 'nearby')


def seperate_con(conversation):
    if not isinstance(conversation,list):
        raise TypeError('conversaiton is not a list')
    operator = []
    reporter = []
    for i in range(0, len(conversation)):
        if i % 2 == 0:
            operator.append(conversation[i])
        else:
            reporter.append(conversation[i])
    if len(reporter) != len(operator):
        if len(reporter) < len(operator):
            reporter.append('')
        else:
            operator.append('')
        # raise ValueError('conversation isnt seperated fairly')
    return operator, reporter


def find_address(ques, ans):
    loc_1 = []
    street_info = []
    district_info= []
    detail_info = []
    nearby_info = []
    for key, ele in enumerate(ques):
        temp_street = [ans[key] for element in street_key if element in ele]
        temp_district = [ans[key] for element in district_key if element in ele]
        temp_nearby = [ans[key] for element in nearby_loc_key if element in ele]
        temp_detail = [ans[key] for element in detail_loc_key if element in ele]
        ans_temp_street = [ans[key] for element in street_key if element in ans[key]]
        ans_temp_district = [ans[key] for element in district_key if element in ans[key]]
        ans_temp_nearby = [ans[key] for element in nearby_loc_key if element in ans[key]]
        ans_temp_detail = [ans[key] for element in detail_loc_key if element in ans[key]]
        street_info.extend(temp_street) if temp_street else ''
        street_info.extend(ans_temp_street) if ans_temp_street else ''
        district_info.extend(temp_district) if temp_district else ''
        district_info.extend(ans_temp_district) if ans_temp_district else ''
        detail_info.extend(temp_detail) if temp_detail else ''
        detail_info.extend(ans_temp_detail) if ans_temp_detail else ''
        nearby_info.extend(temp_nearby) if temp_nearby else ''
        nearby_info.extend(ans_temp_nearby) if ans_temp_nearby else ''
    street_info = list(set(street_info))
    district_info = list(set(district_info))
    detail_info = list(set(detail_info))
    nearby_info = list(set(nearby_info))
    # loc_1 = list(set(loc_1))
    return street_info, district_info, detail_info, nearby_info


if __name__ == '__main__':
    for i in range(1, 4):
        name = str(i) + '.txt'
        file_lines = read_txt_files(name)
        ope, rep = seperate_con(file_lines)
        street, dis, detail, nearby = find_address(ope, rep)
        #print(street)
        #print(dis)
        print(detail)
        #print(nearby)
        print('the ' +str(i)+' conversation finish extracted')

