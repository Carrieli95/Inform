import lda
import numpy as np
from lda_experiment.read_competition_files import *
from lda_experiment.pre_process_texts import seperate_data_set

''' 1.导入数据源 '''
content, titles, id = seperate_data_set('context_train_test_0.txt')
content_1, titles_1, id_1 = seperate_data_set('content_train_test_1.txt')
content = content.extend(content_1)
titles = titles.extend(titles_1)
id = id.extend(id_1)

for i in range(395):
    print(titles[i])


''' 2.求解P(词语|主题),得到每个主题所包含的单词的分布 '''
X = lda.datasets.load_reuters()
vocab = lda.datasets.load_reuters_vocab()
titles = lda.datasets.load_reuters_titles()
# 设置主题数目为20个，每个主题包含8个词语，模型迭代次数为1500次
model = lda.LDA(n_topics=4, n_iter=1500,random_state=1)
model.fit(X)
topic_word = model.topic_word_
n_top_words = 8

for i,topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    # 输出每个主题所包含的单词的分布
    print('Topic{}:{}'.format(i, ' '.join(topic_words)))

''' 3.求解P(主题|文档),得到文章所对应的主题 '''
doc_topic = model.doc_topic_
for i in range(20):
    # 输出文章所对应的主题
    print("{} (top topic:{})".format(titles[i], doc_topic[i].argmax()))