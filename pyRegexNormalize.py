#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

##########################################
#######ע������:############
#######1.&amp;��XML�����ַ�
#######2.��������ʽ��,()�����������Ҫ��Ϊ\(\)
#######3.һ����˵,Voice���б�����text,�����޷��������庬��
##############
##########################################
###��Ҫ��װlxml���ⲿ��
from xml.etree.ElementTree import XMLParser, Comment
import xml.etree.ElementTree as ET

import pyString
import pyUsage
import pyIO

def readPinyinXml(path):
    print(pyUsage.get_cur_info(), 'path= ', path)
    parser01 = XMLParser(encoding='gbk')
    
    ###��תΪutf-16��ʽ
    c_list = pyIO.read_file_content(path)
  
    flag = 'encoding="GBK"'
    flag.lower()
    pos = [i for i,e in enumerate(c_list) if e.find(flag) != -1]
    #print('pos= ', pos)
    
    if len(pos) == 0:
        s_flag = 'encoding=\'gbk\''
        pos = [i for i,e in enumerate(c_list) if e.find(s_flag) != -1]
        if len(pos) > 0:
            c_list[pos[0]] = c_list[pos[0]].replace('\'gbk\'', '"GBK"')
            #print(' 2 pos= ', pos)
    if len(pos) == 0:
        s_flag = 'encoding=\'GBK\''
        pos = [i for i,e in enumerate(c_list) if e.find(s_flag) != -1]
        c_list[pos[0]] = c_list[pos[0]].replace('\'GBK\'', '"GBK"')
        #print(' 3 pos= ', pos)

    #c_list[pos[0]].replace('encoding="GBK"', 'encoding="utf-8"')
    #print ('           item= ', c_list[pos[0]])
    t = '\n'.join(c_list)

    ###��������
    root = ET.fromstring(t)
    
    ###�ļ�ͷ
    lang = ''
    name = ''
    for i,child in enumerate(root[:1]):
        l = child.find('DictionaryLanguage')
        lang= l.text
        n = child.find('DictionaryName')
        name = n.text
    
    ###��������
    word_info_list = []
    for i,child in enumerate(root[1:]):
        ###���ҵ���
        word = child.find('Word')
        #print(word.text)

        ###����ƴ��
        pro_list = []
        for rank in child.iter('TYPE_PURE_NUMBER'):
            t1 = rank.find('0').text
            #print(t1.text)
            t2 = rank.find('1').text
            #print(t1.text)
            t3 = rank.find('2').text
            #print(t1.text)
            t4 = rank.find('BianDiao').text
            #print(t1.text)
            if not t1:
                t1 = ''
            if not t2:
                t2 = ''
            if not t3:
                t3 = ''
            if not t4:
                t4 = ''
            
            tmp_dict = {
                    'ProID':        t1,
                    'PartOfSpeech': t2,
                    'PinYin':       t3,
                    'BianDiao':     t4,
                    }
            pro_list.append(tmp_dict)
            if not t3:
                print(word.text, tmp_dict)
                sys.exit(0)      

        pro_list = singleItem(pro_list)
        word_info_list.append((word.text, pro_list))

    return lang, name, word_info_list

def prettyXml(element, indent, newline, level = 0): # elemntΪ��������Elment�࣬����indent����������newline���ڻ���  
    if element:  
        ############################## �ж�element�Ƿ�����Ԫ��  
        if element.text == None or element.text.isspace(): 
            ############################## ���element��textû������  
            element.text = newline + indent * (level + 1)    
        else:  
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)  
    else:  
        ############################## �˴����������ע��ȥ����Element��textҲ������һ��  
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level  
        pass
    temp = list(element) 
    ############################## ��elemntת��list  
    
    for subelement in temp:  
        if temp.index(subelement) < (len(temp) - 1): 
            ############################## �������list�����һ��Ԫ�أ�˵����һ������ͬ����Ԫ�ص���ʼ������Ӧһ��  
            subelement.tail = newline + indent * (level + 1)  
        else:  
            ############################## �����list�����һ��Ԫ�أ� ˵����һ����ĸԪ�صĽ���������Ӧ����һ��  
            subelement.tail = newline + indent * level  
        prettyXml(subelement, indent, newline, level = level + 1) # ����Ԫ�ؽ��еݹ����  
          
# from xml.etree import ElementTree      #����ElementTreeģ��  
# tree = ElementTree.parse('test.xml')   #����test.xml����ļ������ļ�����������  
# root = tree.getroot()                  #�õ���Ԫ�أ�Element��  
# prettyXml(root, '\t', '\n')            #ִ����������  
# ElementTree.dump(root)                 #��ʾ���������XML����

def addNumber(root):
    id_value = 0    
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'һ,��,One,First')
    d.set('ContentType', 'Number')
    d.set('Model', 'regexNormalize_Number_1.crf_model')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '1'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Kanji')
        e.text = '��'
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '��,��,Two')
    d.set('ContentType', 'Number')
    d.set('Model', 'regexNormalize_Number_2.crf_model')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '2'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', '��')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', '��')
        e.text = '��'
        
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '���,����')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[1-9][0-9]{0,3}'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Year')
        e.text = '{Number(Bit)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '�·�,���,����,ֵΪ1~12')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '([1-9]|1[0-2])'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Month')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Year')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '��������')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[1-9]\d{5,7}'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Telephone')
        e.text = '{Number(Telephone)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    ###2
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '�ֻ�����')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[1]\d{10}'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Telephone')
        e.text = '{Number(Telephone)}'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '����')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}'
    
def addNumber2English(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '3a')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d[a-zA-Z]'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Bit)}{English(Bit)}'

def addNumber2Punctuation(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '�ٷ���')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+%'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'ChinesePrecent')
        e.text = '�ٷ�֮{Number(Count)}'
        e = ET.SubElement(d, 'Voice')

    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '����')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+.*'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(BitIgnorePunctuation)}'

def addNumber2Kanji(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '����')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+��'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit+Kanji')
        e.text = '{Number(Count)}��'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Year')
        e.text = '{Number(Bit)}��'
        e = ET.SubElement(d, 'Voice')

    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '����')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+.*'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count+Kanji')
        e.text = '{Number(Count)}{Kanji}'

def addNumber2Punctuation2Number2Punctuation2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '2,377,155')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+,\d+,\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'CountIgnorePunctuation')
        e.text = '{Number(CountIgnorePunctuation)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '9:26:01')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+:\d+:\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '{Number(Count)}��{Number(Count)}��{Number(Count)}��'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '2007-10-31')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d{4,4}-\d{1,2}-\d{1,2}'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Date')
        e.text = '{Number(Count)}��{Number(Count)}��{Number(Count)}��'

# def addNumber2Punctuation2Number2Punctuation(root):
#     id_value = 0
#     c = ET.SubElement(root, 'ElementEntry')
#     c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
#     t_list = pyUsage.get_cur_info()
#     c.set('TextType', t_list[1].replace('add', ''))
#     ###1
#     d = ET.SubElement(c, 'Node')
#     d.set('Comment', '30%~40%(�ٷ�������)')
#     d.set('ContentType', 'Regex')
#     id_value += 1
#     d.set('ID', '%d'%(id_value))
#     d.text = '\d+%\~\d+%'
#     if True:
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'PercentInterval')
#         e.text = '�ٷ�֮{Number(Count)}���ٷ�֮{Number(Count)}'
            
def addNumber2Punctuation2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'ʱ��,�ȷ�')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+:\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '{Number(Count)}��{Number(Count)}��'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Score2Score')
        e.text = '{Number(Count)}��{Number(Count)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'ʱ��,�ȷ�')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+-\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '{Number(Count)}��{Number(Count)}��'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Count')
        e.text = '{Number(Count)}��{Number(Count)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'ʱ��,�ȷ�')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\d+.\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'DecimalChinese')
        e.text = '{Number(Count)}��{Number(Count)}'
    
# def addNumber2Punctuation2English(root):
#     id_value = 0
#     c = ET.SubElement(root, 'ElementEntry')
#     c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
#     t_list = pyUsage.get_cur_info()
#     c.set('TextType', t_list[1].replace('add', ''))
#     ###1
#     d = ET.SubElement(c, 'Node')
#     d.set('Comment', 'ʱ��,�ȷ�')
#     d.set('ContentType', 'Regex')
#     id_value += 1
#     d.set('ID', '%d'%(id_value))
#     d.text = '\d+:\d+'
#     if True:
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'Time')
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'Score2Score')
# 
def addPunctuation(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'Ц������')
    d.set('ContentType', 'StringValue')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = ':)'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Kanji')
        e.text = 'Ц��'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '<')
    d.set('ContentType', 'StringValue')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '<'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Kanji')
        e.text = 'С��'
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Puctuation')
        e.text = ''

# def addPunctuation2Number2Kanji(root):
#     id_value = 0
#     c = ET.SubElement(root, 'ElementEntry')
#     c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
#     t_list = pyUsage.get_cur_info()
#     c.set('TextType', t_list[1].replace('add', ''))
#     ###1
#     d = ET.SubElement(c, 'Node')
#     d.set('Comment', '(2013��')
#     d.set('ContentType', 'Regex')
#     id_value += 1
#     d.set('ID', '%d'%(id_value))
#     d.text = '\(\d+(��|��)'
#     if True:
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'Redirect')
            
# def addPunctuation2Number2English(root):
#     id_value = 0
#     c = ET.SubElement(root, 'ElementEntry')
#     c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
#     t_list = pyUsage.get_cur_info()
#     c.set('TextType', t_list[1].replace('add', ''))
#     ###1
#     d = ET.SubElement(c, 'Node')
#     d.set('Comment', '��-35S')
#     d.set('ContentType', 'Regex')
#     id_value += 1
#     d.set('ID', '%d'%(id_value))
#     d.text = '-\d+[A-Z]'
#     if True:
#         e = ET.SubElement(d, 'Voice')
#         e.set('ReadType', 'BitIgnorePunctuation')
        
def addPunctuation2Number2Punctuation(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '(000936)��Ʊ֤ȯ����')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '\(\d+\)'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'NumberBit')
        e.text = '{Number(Count)}'
    
def addPunctuation2English2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '&nbsp1938/nx')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '&nbsp\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '{Number(Count)}'

def addPunctuation2Number2Punctuation2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '"9:25 �� -9:30 �� ֮��')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '-\d+:\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Time')
        e.text = '��{Time}'

def addKanji(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'mg')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[^0-9a-zA-Z].*'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Kanji')
        e.text = '{Kanji}'
            
def addEnglish(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'mg')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[a-zA-Z]+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Unit')
        e.text = '{English(Unit)}'

def addEnglish2Number(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', 'JX06323')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[a-zA-Z]+\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Bit')
        e.text = '{English(Bit)}{Number(Bit)}'
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '����,�쳵,�Ǽ��г�D632')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '[a-zA-Z]+\d+'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'Bit')
        e.text = '{English(Bit)}{Number(Bit)}'

def addComplicatedText(root):
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###1
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '�����ʼ�')
    d.set('ContentType', 'Regex')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    d.text = '.*@.*'
    if True:
        e = ET.SubElement(d, 'Voice')
        e.set('ReadType', 'EMail')
        e.text = '{ComplicatedText(Email)}'

def addCombinationText(root):
    ###����+ʱ��
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))

    d = ET.SubElement(c, 'Node')
    d.set('Comment', '����+ʱ��')
    d.set('ContentType', 'Part')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    if True:
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', '����')
        e.set('ContentType', 'TextType')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = 'Number2Punctuation2Number2Punctuation2Number'
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', 'ʱ��')
        e.set('ContentType', 'TextType')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = 'Number2Punctuation2Number2Punctuation2Number'
    
    id_value = 0
    c = ET.SubElement(root, 'ElementEntry')
    c.set('Comment', 'Ĭ��˳����:�Ⱦ���,������;�ȶ̺�')
    t_list = pyUsage.get_cur_info()
    c.set('TextType', t_list[1].replace('add', ''))
    ###����+����+ʱ��
    d = ET.SubElement(c, 'Node')
    d.set('Comment', '����+����+ʱ��')
    d.set('ContentType', 'Part')
    id_value += 1
    d.set('ID', '%d'%(id_value))
    
    if True:
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', '����')
        e.set('ContentType', 'Regex')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = ':'
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', '����')
        e.set('ContentType', 'TextType')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = 'Number2Punctuation2Number2Punctuation2Number'
        ###1
        e = ET.SubElement(d, 'Part')
        e.set('Comment', 'ʱ��')
        e.set('ContentType', 'TextType')
        id_value += 1
        e.set('ID', '%d'%(id_value))
        if True:
            e.text = 'Number2Punctuation2Number2Punctuation2Number'

def addComment(root, text):
    ###����+ʱ��
    comment = ET.Comment(text)
    root.append(comment)
###########################################################################    
def saveRegexNormalizeConfig(file_name):
    ###����xml�ļ�
    a = ET.Element('Dictionary')
    if True:
        addComment(a, "�����ǻ�������:�������೤��<=5")
        ###################################### Number2Kanji
        addNumber2Kanji(a)
        ###################################### Number2Number
        addNumber(a)
        ###################################### Number2English
        addNumber2English(a)
        ###################################### Number2Punctuation
        addNumber2Punctuation(a)
        ###################################### Number2Punctuation2Number
        addNumber2Punctuation2Number(a)
#         ###################################### Number2Punctuation2Number2Punctuation
#         addNumber2Punctuation2Number2Punctuation(a)
        ###################################### addNumber2Punctuation2Number2Punctuation2Number
        addNumber2Punctuation2Number2Punctuation2Number(a)
#         ###################################### Number2Punctuation2English
#         addNumber2Punctuation2English(a)
        ###################################### Punctuation
        addPunctuation(a)
#         ###################################### Punctuation2Number2English
#         addPunctuation2Number2English(a)
#         ###################################### Punctuation2Number2Kanji
#         addPunctuation2Number2Kanji(a)
        ###################################### Punctuation2Number2Punctuation
        addPunctuation2Number2Punctuation(a)
        ###################################### Punctuation2English2Number
        addPunctuation2English2Number(a)
        ###################################### Punctuation2Number2Punctuation2Number
        addPunctuation2Number2Punctuation2Number(a)
        ###################################### Kanji
        addKanji(a)     
        ###################################### English
        addEnglish(a)     
        ###################################### English2Number
        addEnglish2Number(a)
    #######################################
    addComment(a, "�����Ǹ�������:��������ʼ�,�������")
    if True:
        addComplicatedText(a)
        pass
    #######################################
    addComment(a, "�����������������:����Date+Time,�����ʽ����")
    if True:
        #####
        addCombinationText(a)
        pass
        
        
    prettyXml(a, '\t', '\n')
    text = ET.tostring(a, encoding="gbk", method="xml")
    text = text.decode('gbk')
    
    
    pyIO.clear_to_file(file_name)
    pyIO.add_to_file(file_name, text)
