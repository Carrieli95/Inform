from pro_utils.read_files import read_excel_files, read_txt_files_as_whole
from configparser import ConfigParser
from classification_model.classification_test import linear_svc_accuracy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import os
from sklearn.externals import joblib

filename = 'event_info.xlsx'
# filename = 'Repeat_event.xlsx'
invalid = {'hkjkkj', '1241241', '124124', 'test1', 'test2', 'test15', 'test13', '23123', '12321','sfdfdsfd',
              'ddfdfd', 'sddhjdh', 'aaaaaaaaaaaaaaa', 'ghhhhh', 'gfdgdgdggdgd', 'test11', '123123',
              'asdasd', 'sdfdf', '1231231'}

cfg = ConfigParser()
cfg.read('address.ini')
excel_path = cfg.get('document_path', 'excel_path')
txt_path = cfg.get('document_path', 'doc_path')
model_dir = cfg.get('document_path', 'model_dir')
model_path = os.path.join(model_dir, 'event_type_model.pkl')
all_event_sheet = read_excel_files(filename, excel_path)


def prepare_event_with_type(data_list):
    info = data_list['IncidentDescription']
    invalid_check = data_list['InvalidIncidentTypeName']
    type_id = data_list['IncidentTypeId']
    event_grade_id = data_list['IncidentGradeId']
    event_list = []
    type_list = []
    grade_list = []
    for key, ele in enumerate(info):
        if invalid_check[key] != 'Invalid':
            if (not isinstance(ele, float)) and len(ele) >= 6 and (ele not in invalid):
                event_list.append(info[key])
                type_list.append(type_id[key])
                grade_list.append(event_grade_id[key])
        else:
            event_list.append(ele)
            type_list.append(0)
            grade_list.append(0)
    return event_list, type_list, grade_list


def save_model_paras(event_sheet):
    pre_event, event_type, _ = prepare_event_with_type(event_sheet)
    vect = CountVectorizer()
    tf_trans = TfidfTransformer(smooth_idf=False, use_idf=False)
    vector = vect.fit_transform(pre_event).toarray()
    tf = tf_trans.fit_transform(vector).toarray()
    _ = linear_svc_accuracy(tf, event_type, 0.3, model_path)
    return vect, tf_trans


def _to_predict(train_data, predict_data, model_path):
    """
    预测文本分类结果
    :param data: list object, 存储文本分词后的结果
    :return:
    """
    classify_model = joblib.load(model_path)
    vectorizer, tfidftransformer = save_model_paras(train_data)
    vect = vectorizer.transform(predict_data).toarray()
    tf = tfidftransformer.transform(vect).toarray()
    prediction = classify_model.predict(tf)
    prediction = prediction.tolist()
    print(prediction)


if __name__ == "__main__":
    # pre_event, event_type, _ = prepare_event_with_type(all_event_sheet)
    # event = CountVectorizer().fit_transform(pre_event).toarray()
    # event_array = TfidfTransformer(smooth_idf=False, use_idf=False).fit_transform(event).toarray()  # 数据的tf信息
    # test_score = linear_svc_accuracy(event_array, event_type, 0.3, model_path)

    need_to_predict_list = []
    # for i in range(1, 13):
    #     read_txt_name = str(i)+'_span.txt'
    #     predict_content = read_txt_files_as_whole(txt_path, read_txt_name)
    #     need_to_predict_list.append(predict_content)
    for i in range(1, 13):
        read_txt_name = str(i)+'_span.txt'
        predict_content = read_txt_files_as_whole(txt_path, read_txt_name)
        need_to_predict_list.append(predict_content)
    _to_predict(all_event_sheet, need_to_predict_list, model_path)

