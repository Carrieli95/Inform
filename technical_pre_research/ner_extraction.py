import os
import sys

from collections import defaultdict
from datetime import datetime
from fool import ner, cut
import re


class FoolNerBasedExtraction:
    """
    基于FoolNLTK模式的抽取,单例模式
    """
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def ner_info_selector(self, ner_results, *keys, all_flag=True) -> dict:
        # 有keys的时候优先keys里的arguments
        res = defaultdict(lambda: [])
        if all_flag and len(keys) != 0:
            all_flag = False

        if not all_flag:
            # 走keys里的参数
            keys = list(keys)
            for index, ele in enumerate(keys):
                # 预处理keys参数
                if not isinstance(ele, str):
                    raise ValueError("Key must be str type")
                else:
                    keys[index] = keys[index].strip()
            location_flag = 0
            for ner_res in ner_results:
                # 节省时间
                if not keys:
                    break
                for key_ele in keys:
                    if ner_res[2] == key_ele:
                        res[key_ele].append((ner_res[3], ner_res[0:2], ner_res[2]))
            return res

        # all_flag is true, we return all existing results
        for ner_res in ner_results:
            res[ner_res[2]].append((ner_res[3], ner_res[0:2], ner_res[2]))
        return res

    @staticmethod
    def _location_generation(location_info, raw_text):
        res = defaultdict(lambda: [])
        tem_res = []
        pre_res =[]
        location_flag = 0
        company_location_flag = 0
        org_location_flag = 0
        for key in location_info.keys():
            tem_res.extend(location_info[key])
        tem_res = sorted(tem_res, key=lambda x: x[1])
        for ele in tem_res:
            if len(raw_text) != ele[1][1]-1:
                if ele[2] == 'location' and (raw_text[ele[1][1]-1] == '人' or raw_text[ele[1][1]-1] == '籍'):
                    continue
                pre_res.append(ele)
            else:
                # if ele[2] == 'location':
                #     continue
                pre_res.append(ele)
        position = None
        key = ''
        location_counter = ''
        company_counter = ''
        org_counter = ''
        for ele in pre_res:
            if 'location' in ele[2]:
                location_counter = 'location'
            if 'company' in ele[2]:
                company_counter = 'company'
            if 'org' in ele[2]:
                org_counter = 'org'
        if location_counter == 'location':
            for ele in pre_res:
                if ele[2] == 'location' and location_flag == 0:
                    location_flag = 1
                    key = ele[2]
                    temp = ele[1]
                    position = temp
                    res[key].append(ele[0])
                elif (ele[2] == "company" or ele[2] == "org" or ele[2] == 'location') and location_flag == 1:
                    location_flag = 0
                    tem_position = ele[1]
                    temp_res = ele[0]
                    if (abs(min(tem_position) - max(position)) <= 2) and (raw_text[position[1]-1] != ' ' and
                                                                   raw_text[position[1]-1] != '。' and
                                                                   raw_text[position[1]-1] != '、'):
                        if abs(min(tem_position) - max(position)) == 0:
                            if raw_text[position[1]-1] == '(':
                                res[key][-1] = res[key][-1] + raw_text[position[1] - 1] + temp_res + raw_text[tem_position[1] - 1:raw_text.find(')',tem_position[1])+1]
                            else:
                                res[key][-1] = res[key][-1] + raw_text[position[1]-1] + temp_res
                        if abs(min(tem_position) - max(position)) == 1:
                            res[key][-1] = res[key][-1] + raw_text[position[1]-1:position[1]+1] + temp_res
                        if abs(min(tem_position) - max(position)) == 2:
                            res[key][-1] = res[key][-1] + raw_text[position[1]-1:position[1]+2] + temp_res
                        location_flag = 1
                        position = (min(position),max(tem_position))
                    elif ele[2] == 'location' and location_flag == 0:
                        location_flag = 1
                        key = ele[2]
                        temp = ele[1]
                        position = temp
                        res[key].append(ele[0])

                if ele[2] == 'company' and location_flag == 0 and company_location_flag == 0 and org_location_flag == 0:
                    company_location_flag = 1
                    c_key = ele[2]
                    c_temp = ele[1]
                    c_position = c_temp
                    res[c_key].append(ele[0])
                elif (ele[2] == 'location') and company_location_flag == 1:
                    company_location_flag = 0
                    c_tem_position = ele[1]
                    c_temp_res = ele[0]
                    if (abs(min(c_tem_position) - max(c_position)) <= 2) and (raw_text[c_position[1]-1] != ',' and
                                                                   raw_text[c_position[1]-1] != '。' and
                                                                   raw_text[c_position[1]-1] != '、'):
                        if abs(min(c_tem_position) - max(c_position)) == 0:
                            res[c_key][-1] = res[c_key][-1] + raw_text[c_position[1]-1] + c_temp_res
                        if min(c_tem_position) - max(c_position) == 1:
                            res[c_key][-1] = res[c_key][-1] + raw_text[c_position[1]-1:c_position[1]+1] + c_temp_res
                        elif min(c_tem_position) - max(c_position) == -1:
                            res[c_key][-1] = res[c_key][-1] + c_temp_res
                        if min(c_tem_position) - max(c_position) == 2:
                            res[c_key][-1] = res[c_key][-1] + raw_text[c_position[1]-1:c_position[1]+2] + c_temp_res
                        elif min(c_tem_position) - max(c_position) == -2:
                            res[c_key][-1] = res[c_key][-1] + c_temp_res
                        res['location'].append(res[c_key][-1])
                        company_location_flag = 1
                        c_position = (min(c_position), max(c_tem_position))
                    elif ele[2] == 'company':
                        company_location_flag = 1
                        c_key = ele[2]
                        c_temp = ele[1]
                        c_position = c_temp
                        res[c_key].append(ele[0])

                if ele[2] == 'org' and location_flag == 0 and company_location_flag == 0 and org_location_flag == 0:
                    org_location_flag = 1
                    o_key = ele[2]
                    o_temp = ele[1]
                    o_position = o_temp
                    res[o_key].append(ele[0])
                elif (ele[2] == 'location') and org_location_flag == 1:
                    org_location_flag = 0
                    o_tem_position = ele[1]
                    o_temp_res = ele[0]
                    if (abs(min(o_tem_position) - max(o_position)) <= 2) and (raw_text[o_position[1]-1] != ',' and
                                                                   raw_text[o_position[1]-1] != '。' and
                                                                   raw_text[o_position[1]-1] != '、'):

                        if abs(min(o_tem_position) - max(o_position)) == 0:
                            res[o_key][-1] = res[o_key][-1] + raw_text[o_position[1]-1] + o_temp_res
                        if min(o_tem_position) - max(o_position) == 1:
                            res[o_key][-1] = res[o_key][-1] + raw_text[o_position[1]-1:o_position[1]+1] + o_temp_res
                        elif min(o_tem_position) - max(o_position) == -1:
                            res[o_key][-1] = res[o_key][-1] + o_temp_res
                        if min(o_tem_position) - max(o_position) == 2:
                            res[o_key][-1] = res[o_key][-1] + raw_text[o_position[1]-1:o_position[1]+2] + o_temp_res
                        elif min(o_tem_position) - max(o_position) == -2:
                            res[o_key][-1] = res[o_key][-1] + o_temp_res
                        res['location'].append(res[o_key][-1])
                        org_location_flag = 1
                        o_position = (min(o_position), max(o_tem_position))
                    elif ele[2] == 'org':
                        org_location_flag = 1
                        o_key = ele[2]
                        o_temp = ele[1]
                        o_position = o_temp
                        res[o_key].append(ele[0])

            return res, location_counter
        elif company_counter == 'company':
            for ele in pre_res:
                if ele[2] == 'company':
                    res[ele[2]].append(ele[0])
            return res, company_counter
        elif org_counter == 'org' and company_counter != 'company':
            for ele in pre_res:
                if ele[2] == 'org' and location_flag == 0:
                    res[ele[2]].append(ele[0])
            return res, org_counter
        elif location_counter == '' and company_counter == '' and org_counter == '':
            return res, ''

    @staticmethod
    def _json_format_generattion(ele, raw_location, tmp_detial, reloc_res, tmp_dict, reloc_dict):
        detail_index = 0
        for lat, addr in zip(ele, raw_location):
            ini_dict = {}
            if lat == '0,0':
                ini_dict["address"] = addr
                ini_dict["detail"] = tmp_detial
                ini_dict["address_latitude_longitude"] = lat
                reloc_dict.append(ini_dict)
            else:
                ini_dict["address"] = addr
                ini_dict["detail"] = reloc_res[detail_index]
                ini_dict["address_latitude_longitude"] = lat
                reloc_dict.append(ini_dict)
                detail_index += 1
        if "address_detail" not in tmp_dict:
            tmp_dict["address_detail"] = []
        tmp_dict["address_detail"].extend(list(reloc_dict))
        return tmp_dict

    # extract_location V2.0
    def extract_location(self, text, first_one=True) -> list:
        ner_results = ner(text, ignore=True)
        for ner_res, raw_text in zip(ner_results, text):
            logger.info("NER result is as follows %s" % ner_res)
            location_info = self.ner_info_selector(ner_res, "location", "company", "org")
            location_info, key_value = self._location_generation(location_info, raw_text)
            location_info = location_info[key_value]
            if first_one and len(location_info) > 0:
                location_info = [location_info[0]]
            if not first_one and len(location_info) > 0:
                location_info = [sorted(location_info, key=lambda x: len(x))[-1].replace(',', '')]
            print(location_info)
        return location_info


if __name__ == '__main__':
    rbe = RuleBasedExtraction()
    test_str = "2008年10月28日20时0分，在重庆市武隆县芙蓉江跨江大桥施工现场，钢丝绳吊斗运送22名工人上晚班，由于平衡物断落，打在吊斗上使其坠落在桥面，当场死亡9人，送医院途中死亡2人，重伤7人，轻伤4人。"

    ddres = rbe.extract_time(datetime.now(), test_str)[0]
    print(ddres)
