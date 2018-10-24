from sklearn import svm, datasets
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
import ast
import re
import numpy as np
from sklearn.externals import joblib


def pre_processing(filename, column):
    """
    读取分词后的文件，并将分词结果改写成英文书写格式，便于后续使用。含有[]的那一版的分词文件专用函数
    :param filename:
    :param column:
    :return:
    """
    data = read_sep_txt_files(filename)[column]
    for key, ele in enumerate(data):
        data[key] = ast.literal_eval(ele)
        data[key] = [i.strip() for i in data[key]]
        data[key] = ' '.join(data[key])
    return data


def normal_pre_processing(filename):
    data = read_txt_files(filename)
    pattern = r'\s{2,3}'
    for key, ele in enumerate(data):
        data[key] = re.sub(pattern, ' ', ele)
    return data


def save_model():
    data_after_token = normal_pre_processing('aj_bj.txt')
    stop_words = read_txt_files('stopword.txt')
    event_type = read_txt_files("aj_with_bj_label.txt")
    vectorizer = CountVectorizer(stop_words=stop_words)
    tfidftransformer = TfidfTransformer(smooth_idf=False, use_idf=False)
    vect = vectorizer.fit_transform(data_after_token).toarray()
    tf = tfidftransformer.fit_transform(vect).toarray()
    kfold_linear_svc_clf = LinearSVC()
    model = kfold_linear_svc_clf.fit(tf, event_type)
    joblib.dump(model, "C:/Users/cong/PycharmProjects/testltp/Event_Classification/sklearn_classification/writeFiles/model.pkl")
    return vectorizer, tfidftransformer


def linear_svc_accuracy(x, y, kn, save_path):
    """
    :param x: array list data for train and test
    :param y: label for x
    :param kn: proportion of sampling. Eg: 0.3
    :return:
    """
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=kn, random_state=None)
    tuned_parameters = {'C': [1, 5]}
    # linear_svc_clf = GridSearchCV(svm.LinearSVC(), param_grid=tuned_parameters, cv=int(kn*10), scoring='f1_macro')
    # scoring='accuracy'
    linear_svc_clf = svm.LinearSVC()  # 保留原版
    model = linear_svc_clf.fit(x_train, y_train)
    joblib.dump(model, save_path)
    # best_parameter = linear_svc_clf.best_params_
    best_parameter = linear_svc_clf.get_params()
    result = linear_svc_clf.score(x_test, y_test)
    print('The accuracy of LinearSVC classification is %s' % result)
    print('Using parameter %s' % best_parameter)
    return result


def kfold_linear_svc_accuracy(x, y, kfold):
    """
    :param x: array list data for train and test
    :param y: label for x
    :param kfold: kfold value
    :return:
    """
    kfold_linear_svc_clf = svm.LinearSVC()
    result = cross_val_score(kfold_linear_svc_clf, x, y, cv=kfold)
    print('The accuracy of Kfold linear SVC classification is %s' % result.mean())
    return result


if __name__ == "__main__":
    # data_after_token = normal_pre_processing('aj_bj.txt')
    stop_words = read_txt_files('stopword.txt')
    data_after_token = normal_pre_processing('all_segment.txt')
    # data_after_token = pre_processing("word_segment_beijing.txt", 0)
    # data_after_token = data_after_token.tolist()
    # raw_data = read_excel_files("usegreen_8700.xlsx")['事件类型']
    # event_type = [ele for ele in raw_data]
    # event_type = read_txt_files("aj_with_bj_label.txt")

    event_type = read_txt_files("all_label.txt")
    # # 完成对读取数据的预处理
    # # TODO: 在剔除实体和地点的时候，是否可以考虑chunk标注和正则的结合，直接拿掉结果，进而避免二次分词，提高效率

    vect = CountVectorizer(stop_words=stop_words).fit_transform(data_after_token).toarray()
    tf = TfidfTransformer(smooth_idf=False, use_idf=False).fit_transform(vect).toarray()  # 数据的tf信息
    save_model()

    # np.savetxt('查看输出结果.txt', tf)
    # LSvc_accuracy = linear_svc_accuracy(tf, event_type, 0.3)
    # result = kfold_linear_svc_accuracy(tf, event_type, 5)  # K-fold Linear_svc模型分类结果


# # pipeline 方式的交叉验证
# SVM = Pipeline([
#                 ('vect', CountVectorizer(stop_words=stop_words, max_df=1.0, min_df=1)),
#                 ('tf', TfidfTransformer(norm='l2', use_idf=False)),
#                 #('pca',PCA(n_components=2000)),
#                 # ('sel', SelectKBest(chi2, k=2000)),
#                 #('sel', SelectKBest(mutual_info_classif,k=1000)),
#                 ('clf', LinearSVC())])
#
# results = cross_val_score(SVM, data_after_token, event_type, cv=5)
# # 交叉验证代码
# print("KFold LinearSVC classification accuracy is %s" % results.mean())
#
# X_train, X_test, y_train, y_test = train_test_split(data_after_token, event_type, test_size=0.3,
#                                                     random_state=None)
#
# SVM = SVM.fit(X_train, y_train)
# prediction = SVM.predict(X_test)
# scores = SVM.score(X_test, y_test)
# print(scores)


