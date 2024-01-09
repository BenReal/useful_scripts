#coding:utf8
import os
import sys
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 如果当前目录是 'useful_scripts'，将当前目录加入搜索路径，否则，将父目录加入搜索路径
if os.path.basename(script_dir) == 'useful_scripts':
    sys.path.append(script_dir)
else:
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(parent_dir)
# 导入其他模块
import shutil
import logging
import time
from local_modules.local_functions import configure_logging
import math
import jieba
import jieba.analyse
import codecs
import re
import csv
import pandas as pd
import docx
from docx import Document

log_file_path = r'../logs/app.log'
configure_logging(log_file_path)

# 记录日志信息
logging.info('程序开始运行')


class SimHash(object):

    def __init__(self):
        pass

    def getBinStr(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            # print(source, x)

            return str(x)

    def getWeight(self, source):
        # fake weight with keyword
        return ord(source)

    def unwrap_weight(self, arr):
        ret = ""
        for item in arr:
            tmp = 0
            if int(item) > 0:
                tmp = 1
            ret += str(tmp)
        return ret

    def simHash(self, rawstr):
        seg = jieba.cut(rawstr, cut_all=True)
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=100, withWeight=True)
        # print(keywords)
        ret = []
        for keyword, weight in keywords:
            binstr = self.getBinStr(keyword)
            keylist = []
            for c in binstr:
                weight = math.ceil(weight)
                if c == "1":
                    keylist.append(int(weight))
                else:
                    keylist.append(-int(weight))
            ret.append(keylist)
        # 对列表进行"降维"
        # print(ret)
        rows = len(ret)
        cols = len(ret[0])
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        return "".join(result)

    def getDistance(self, hashstr1, hashstr2):
        length = 0
        for index, char in enumerate(hashstr1):
            if char == hashstr2[index]:
                continue
            else:
                length += 1
        return length

    def getMaxCommonSubstr(self, s1, s2):
    # 求两个字符串的最长公共子串
    # 思想：建立一个二维数组，保存连续位相同与否的状态
        len_s1 = len(s1)
        len_s2 = len(s2)
        # 生成0矩阵，为方便后续计算，多加了1行1列
        # 行: (len_s1+1)
        # 列: (len_s2+1)
        record = [[0 for i in range(len_s2+1)] for j in range(len_s1+1)]           
        maxNum = 0          # 最长匹配长度
        p = 0               # 字符串匹配的终止下标 
        for i in range(len_s1):
            for j in range(len_s2):
                if s1[i] == s2[j]:
                    # 相同则累加
                    record[i+1][j+1] = record[i][j] + 1
                    
                    if record[i+1][j+1] > maxNum:
                        maxNum = record[i+1][j+1]
                        p = i # 匹配到下标i
        # 返回 子串长度，子串
        return maxNum, s1[p+1-maxNum : p+1]
    def get_zh_num(self, s):
        '包含汉字的返回TRUE'
        n = 0
        for c in s:
            if '\u4e00' <= c <= '\u9fa5':
                n += 1
        return n


if __name__ == "__main__":

    with codecs.open('./useful_scripts/config/config.txt', 'r', encoding='utf8') as configs:
        lines = configs.readlines()
        dic = {}
        for line in lines:
            if line:
                words = line.split(':')
                dic[words[0].strip()] = words[1].strip()

    inpath = dic['inpath']
    outpath = dic['outpath']
    min_length_para = int(dic['min_length_para'])
    min_length_sent = int(dic['min_length_sent'])
    min_dist = int(dic['min_dist'])
    max_common = int(dic['max_common'])

    print('参数配置：',dic)

    document = Document(inpath)
    lines = [para.text for para in document.paragraphs]
    lines_cut = []
    for m in range(len(lines)):
        # if lines[m].strip() == '主要参考文献' and lines[m+1][:3] == '[1]':
        if lines[m].strip() == '主要参考文献':
            break
        else:
            lines_cut.append(lines[m])
    lines_cut = [i.replace('\r\n','\n') for i in lines_cut if len(i) > min_length_para]

    sents = []
    for j in lines_cut:
        t = j.split('。')
        t = [i for i in t if len(i) > min_length_sent]
        sents.extend(t)   
    # for j in lines_cut:
    #     temp = []
    #     t = j.split('。')
    #     for k in t:
    #         l = k.split('；')
    #         temp.extend(l)
    #     temp = [i for i in temp if len(i) > min_length_sent]
    #     sents.extend(temp)
    print(len(sents))

    simhash = SimHash()
    df = pd.DataFrame(columns=['最长公共子串','差异程度','句子1','句子2'])
    for k in range(len(sents)):
        print('==================正在比对：',k,'/',len(sents))
        for l in range(k+1, len(sents)):
            # print(k)
            set1 = set(sents[k])
            set2 = set(sents[l])
            set3 = set1 & set2
            n = min(len(set1), len(set2))
            if len(set3) < n*0.5:
                continue
            try:
                hash1 = simhash.simHash(sents[k])
                hash2 = simhash.simHash(sents[l])
                common = simhash.getMaxCommonSubstr(sents[k],sents[l])
                distance = simhash.getDistance(hash1,hash2)
                if distance <= min_dist:
                    print('句子1：',sents[k])
                    print('句子2：',sents[l])
                    print('差异程度：',distance)
                    print('最长公共子串:',common[1])
                    row = {'最长公共子串':common[1],'差异程度':distance,'句子1':sents[k],'句子2':sents[l]}
                    df = df.append([row], ignore_index=True )
                elif common[0] > max_common and simhash.get_zh_num(common[1]) > 2:
                    print('句子1：',sents[k])
                    print('句子2：',sents[l])
                    print('差异程度：',distance)
                    print('最长公共子串:',common[1])
                    row = {'最长公共子串':common[1],'差异程度':distance,'句子1':sents[k],'句子2':sents[l]}
                    df = df.append([row], ignore_index=True )
            except:
                continue
    # print(df)
    df = df.sort_values(by='差异程度')
    df = df.drop_duplicates()
    # print(type(df))
    df.to_excel(outpath,index =False)


# 环境准备：
# 1、安装anaconda
# https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/
# 2、安装所需软件包
# pip install jieba
# pip install docx


