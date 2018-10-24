from lda_experiment.read_competition_files import *


def seperate_data_set(filename):
    try:
        content_only = []
        title_only = []
        id_only = []
        text = read_context_from_test(filename)
        data_list = pre_processing(text)
        for ele in data_list:
            content_only.append(ele['content'])
            title_only.append(ele['title'])
            id_only.append(ele['id'])
        return content_only, title_only, id_only
    except Exception as e:
        print('Error from content_only' + str(e))


if __name__ == "__main__":
    just_content,_,_ = seperate_data_set('context_train_test_0.txt')
    print(just_content[0:2])