# -*- coding:utf-8 -*-
# @author: xrx
# @time: 2024/3/27 23:05
# @project: SH4NH4I
# @file: amin.py
# @software: PyCharm
# desc:


from datasketch import MinHash
import jieba


def text_to_words(text):
    """将中文文本分词成词的集合"""
    words = set(jieba.cut(text))
    return words


def calculate_similarity(text1, text2, num_perm=128):
    """计算两段中文文本的相似度"""
    # 将文本分词
    words1 = text_to_words(text1)
    words2 = text_to_words(text2)

    # 初始化MinHash对象
    m1, m2 = MinHash(num_perm=num_perm), MinHash(num_perm=num_perm)

    # 向MinHash对象中添加词
    for word in words1:
        m1.update(word.encode('utf8'))
    for word in words2:
        m2.update(word.encode('utf8'))

    # 计算并返回相似度
    return m1.jaccard(m2)


# 示例中文文本
text1 = "MinHash是一种用于估计数据集相似度的概率数据结构"
text2 = "MinHash是一种快速估计两个集合相似度的技术"

# 计算相似度
similarity = calculate_similarity(text1, text2)
print(f"两段文本的估计相似度为: {similarity:.2f}")
