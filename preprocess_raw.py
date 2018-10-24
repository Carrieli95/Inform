from docx import Document
import os


def write_list_to_txt(alllines, filename):
    path = "/Users/carrie/Documents/辰安信息/数据相关/报警电话翻译/urltxtFiles"
    path = os.path.join(path, filename)
    with open(path, 'w', encoding='utf-8') as file:
        if type(alllines)!= list:
            file.writelines(alllines)
        else:
            for ele in alllines:
                file.writelines(str(ele))
                file.writelines('\n')
    return file


def read_docx_from_local(filename):
    path = "/Users/carrie/Documents/辰安信息/数据相关/报警电话翻译"
    path = os.path.join(path, filename)
    read_txt = Document(path)
    spainish = []
    chinese = []
    count = 0
    for i in read_txt.paragraphs:
        if i.text:
            if count % 2 == 0:
                spainish.append(i.text)
            else:
                chinese.append(i.text)
            count += 1
    print(spainish)
    print(chinese)
    # return chinese
    return chinese


# for i in range(4,13):
#     name = str(i) + '.docx'
#     txt = str(i)+'.txt'
reporter = read_docx_from_local('7.docx')
write_one = write_list_to_txt(reporter, '7.txt')