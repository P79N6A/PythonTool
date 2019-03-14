#!/usr/bin/python
#-*- coding: gb18030 -*-

import sys
import os
import pyUsage
import pyString

###��ÿ���ִʽ���� "��"+"����"��Ϊ2Ԫ��
def extract_word_charactor(element):
#     print('element= ', element)
    pos = element.rfind('/')
    if -1 == pos:
        print(pyUsage.get_cur_info(), 'no split for chara error! element=', element)
        sys.exit(0)
        ###�Է��Ž��м�"/w"����
        if len(element.encode('utf8')) == len(element):
            return [element, 'w']
        elif len(element) > 10:
            print(pyUsage.get_cur_info(), 'error! too much long! element=', element)
            sys.exit(0)
        else:
            return [element, '']
            #sys.exit(0)

    return [element[:pos], element[pos+1:]]

###�ѷ־������ʷֲ�
def split_text(text):
    t_list = text.split(' ')
    t_list = [e.strip() for e in t_list if len(e.strip()) > 0]
    t_list = [extract_word_charactor(e) for e in t_list]
    return t_list

###�ִʵ�ʱ��,"����,Ӣ��,����,����"֮�����ӿո�,�Ӷ����ڷִ�Ԥ����
def addSpaceSeperator(text):
    res = ''
    for i,e in enumerate(text):
        res += e
        if i + 1 < len(text) and isAddSpaceSeperate(e, text[i+1]):
            if len(res) > 0 and res[-1] != ' ':###����2���ո�
                res += ' '
    return res
    
###�Ƿ���Ҫ���ӿո�
###Ӣ��/������һ��
###������һ��
###������һ��
def isAddSpaceSeperate(cur_ch, next_ch):
    ###�����ո�
    if cur_ch == ' ':
        return False
    ###����
    elif pyString.isCharactorSeperator(cur_ch):
        if not pyString.isCharactorSeperator(next_ch):
            return True
    ###Ӣ��,���ֺϲ�
    elif pyString.isCharactorEnglish(cur_ch) or pyString.isCharactorNumber(cur_ch):
        if (not pyString.isCharactorEnglish(next_ch)) \
            and (not pyString.isCharactorNumber(next_ch)):
            return True
    ###����
    else:
        if (pyString.isCharactorSeperator(next_ch)    \
            or pyString.isCharactorEnglish(next_ch) \
            or pyString.isCharactorNumber(next_ch) ):
            return True
        #print('e=|%s|'%e, 'res=|%s|'%res)
    return False

###����BMIѵ������:�ݲ�����Ӣ��,����,����
def genTrainText(text, flag_single_column = False):
    word_list = text.split(' ')
    res_list = []
        
    for i, word in enumerate(word_list):
        t = ''
        if word == ' ' or len(word) == 0:
            pass
        ###Ӣ��/������һ��
        ###������һ��
        ###������һ��
        ###��,���ڵĴʳ���,���,λ�ô����,λ��index����
#################################################��һ���汾,����ԭʼӢ�ĺ�����
#         elif pyString.isAllSeperator(word):
#             res_list.append((word, 1, 'SEPERATOR', 'S'))
#         elif pyString.isAllEnglish(word):
#             res_list.append((word, 1, 'ENGLISH', 'S'))
#         elif pyString.isAllNumber(word):
#             res_list.append((word, 1, 'NUMBER', 'S'))
#         elif pyString.isAllNumberOrEnglish(word):
#             res_list.append((word, 1, 'NUM_ENG', 'S'))
#         ###1��
#         elif len(word) == 1:
#             res_list.append((word, len(word), 'HAN', 'S'))
#         elif len(word) == 2:
#             res_list.append((word[0], len(word), 'HAN', 'B'))
#             res_list.append((word[1], len(word), 'HAN', 'I'))
#         else:
#             res_list.append((word[0], len(word), 'HAN', 'B'))
#             for i,e in enumerate(word[1:-1]):
#                 res_list.append((e, len(word), 'HAN', 'M'))
#             res_list.append((word[-1], len(word), 'HAN', 'I'))
#     ###������ת���ַ���
#     res_list = [list(e[:-1]) + ['%s'%e[-1]] for e in res_list]
#     res_list = [list(e[:1]) + ['%s'%e[1]] + list(e[2:]) for e in res_list]
#     ###�����д����д���
#     labeled_result = []
#     if flag_single_column:
#         labeled_result = ['\t\t'.join(e[:-1]) for e in res_list]
#     else:
#         for e in res_list:
#             #print('e= ', e)
#             labeled_result.append('\t\t'.join(e))
# 
#     res =  '\n'.join(labeled_result)     

#################################################��2���汾,Ӣ��ENG ����NUM
        elif pyString.isAllSeperator(word):
            res_list.append((word, 'S'))
        elif pyString.isAllEnglish(word):
            res_list.append(('ENGLISH', 'S'))
        elif pyString.isAllNumber(word):
            res_list.append(('NUMBER', 'S'))
        elif pyString.isAllNumberOrEnglish(word):
            res_list.append(('NUM_ENG', 'S'))
        ###1��
        elif len(word) == 1:
            res_list.append((word, 'S'))
        elif len(word) == 2:
            res_list.append((word[0], 'B'))
            res_list.append((word[1], 'I'))
        else:
            res_list.append((word[0], 'B'))
            for i,e in enumerate(word[1:-1]):
                res_list.append((e, 'M'))
            res_list.append((word[-1], 'I'))
    ###������ת���ַ���:û������,���账��

    ###����    
    labeled_result = []
    if flag_single_column:
        labeled_result = [' '.join(e[:-1]) for e in res_list]
    else:
        for e in res_list:
            #print('e= ', e)
            labeled_result.append(' '.join(e))

###################################################    

    res =  '\n'.join(labeled_result)     
    return res

#         print('word= ', word)
#         print('res_list= ', res_list)
#     print('text= ', text)
#     print('res=  ', res)

if __name__ == '__main__':
    pass   
