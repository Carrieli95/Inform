from pro_utils.read_files import read_excel_files, read_txt_files
from configparser import ConfigParser
import copy
import spacy
import re
from stop_words import get_stop_words

# filename = 'Repeat_event.xlsx'
filename = 'RepeatIncident_New.xlsx'
nlp = spacy.load("es_core_news_md")
stop_words = {'PROVINCIA', 'CUIDAD', 'PROV/', 'CANTON', 'CUID/', 'Dir', 'DIRECCION', 'EL ALERTANTE INDICA QUE', 'PRUEBA',
             'ALERTANTE INDICA', 'R/.', 'R /', 'R/', 'R:', 'REF/', ':', './', '\r', '\n'}
# stop_words = get_stop_words('spanish')

cfg = ConfigParser()
cfg.read('address.ini')
excel_path = cfg.get('document_path', 'excel_path')
txt_path = cfg.get('document_path', 'doc_path')


all_event_sheet = read_excel_files(filename, excel_path)
des = all_event_sheet['IncidentDescription']
# stop_words = read_txt_files(txt_path, 'span_stop_words.txt')


def _remove_stopwds(info_list, stop_word):
    if isinstance(info_list,list):
        for key, ele in enumerate(info_list):
            for i in stop_word:
                pattern = re.compile(i, re.IGNORECASE)
                info_list[key] = pattern.sub('', info_list[key])
    elif isinstance(info_list, str):
        for i in stop_word:
            pattern = re.compile(i, re.IGNORECASE)
            info_list = pattern.sub('', info_list)
    return info_list


def repeat_appeal_dict(info_list):
    repeat_dict = {}
    null_index = []
    for key, ele in enumerate(info_list):
        if isinstance(ele, float):
            null_index.append(key)
        elif not ele:
            null_index.append(key)
    null_index = set(null_index)
    i = 0
    sample_num = 0
    while i < len(info_list):
        if i not in null_index:
            sample_num += 1
            repeat_tuple_flag = True
            repeat_dict[info_list[i]] = []
            j = 1
            while repeat_tuple_flag:
                if ((i+j) not in null_index) and ((i+j) < len(info_list)):
                    repeat_dict[info_list[i]].append(info_list[i+j])
                    j += 1
                else:
                    i = i+j+1
                    repeat_tuple_flag = False
        else:
            i = i+1
    return repeat_dict, sample_num


def find_similarity(content_list, word_to_remove):
    """
    using word_2_vector and cosine method in spacy kit to compute similarity
    :param content_list:
    :param word_to_remove:
    :return:
    """
    similar_dic = {}
    content = []
    for ele in content_list:
        if not isinstance(ele, float):
            content.append(ele)
    compare_list = copy.deepcopy(content)
    for ele in content:
        target = nlp(_remove_stopwds(ele, word_to_remove))
        temp_similar_dic = {}
        for i in compare_list:
            need_to_compare = nlp(_remove_stopwds(i, word_to_remove))
            similar = target.similarity(need_to_compare)
            temp_similar_dic[i] = similar
        sorted_temp = sorted(temp_similar_dic.items(), key=lambda d: d[1], reverse=True)
        similar_dic[ele] = sorted_temp[1][0]
    return similar_dic


def similar_evaluation(result, standard):
    """
    :param result: dict_object need to evaluate
    :param standard: dic_object need to compared to
    :return: int. value equals to the number of result matches
    """
    count = 0
    not_match = []
    for i in result.keys():
        if i in standard and (result[i] in standard[i]):
            count +=1
        elif i not in standard.keys():
            not_match.append(i)

    return count, not_match


def corpus_similarity(list_1):
    """
    compute similarity from common_corpus perspective
    :param list_1:
    :return:
    """
    similar_dic = {}
    content = []
    for ele in list_1:
        if not isinstance(ele, float):
            content.append(ele)
    compare_list = copy.deepcopy(content)
    for ele in content:
        temp_set = set(ele.split())
        temp_similar_dic = {}
        for i in compare_list:
            need_to_compare = set(i.split())
            common = temp_set.intersection(need_to_compare)
            similar = float(len(common))/(len(temp_set)+len(common)-len(common))
            temp_similar_dic[i] = similar
        sorted_temp = sorted(temp_similar_dic.items(), key=lambda d: d[1], reverse=True)
        similar_dic[ele] = sorted_temp[1][0]
    return similar_dic


if __name__ == "__main__":
    dic, sample_count= repeat_appeal_dict(des)
    print('this is tuple', dic)
    print('total events number', sample_count)
    # result = find_similarity(des, stop_words)
    result = corpus_similarity(des)
    print('this is similar sents', result)
    num, item = similar_evaluation(result, dic)
    print(num)




