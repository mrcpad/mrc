
# !-*-coding:utf-8 -*-


'''
版本 ：v1.0.0
创建 ：xxf at 2019/03/15 9:38
更新内容 ：集合类型的扩展方法

版本 ：v1.0.1
更新 ：xxf at 2019/
更新内容 ：

'''


def where(list, element):
    return [ele for ele in list if ele == element]



def find_index(list, element):
    '''
    返回list中element要素所在的索引
    :param list:
    :param element:
    :return:
    '''
    result_list = []
    index = 0
    for l in list:
        if l == element:
            result_list.append(index)
        index = index + 1

    return result_list


def split_by_index_list(list, index_list):
    '''
    根据索引集合截取list
    :param list:
    :param index_list:
    :param start_index:开始索引 默认 0
    :return:
    '''

    dic = {}
    start_index = 0
    for index in index_list:
        split_list = split(list, start_index, index + 1)
        dic.setdefault(index, split_list)
        start_index = index + 1

    return dic


def split(list, start_index, end_index):
    '''
    根据开始索引和结束截取集合
    :param list:被截取的集合
    :param start_index:开始索引
    :param end_index:结束索引
    :return:
    '''

    split_list = []
    if start_index == -1:
        print("start index can not = -1")
        return split_list
    if end_index > len(list):
        print("end index can not = len(list)")
        return split_list

    for i in range(start_index, end_index):
        split_list.append(list[i])

    return split_list
