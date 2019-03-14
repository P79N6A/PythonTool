#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import sys
import os
import xml.etree.ElementTree as ET
import pyIO

def readPinyinPhonemeDict(path):
    if not path or not os.path.exists(path):
        logging.error('error! path not exists!')
        sys.exit(0)

    c_list = pyIO.read_file_content(path)
    c_list = [e.strip() for e in c_list if len(e.strip()) > 0]
    pair_list = [(e.split(' ')[0], e.split(' ')[1:]) for e in c_list]
    
#     print get_cur_info(), dict(pair_list)
    return dict(pair_list)

def get_han2py_dict(path):
    ###���뺺�ֵ�ƴ���� xml �ļ�
    ###����ע��:���е�GBKҪתΪutf-8
    ###���ö�ȡ�ַ����ķ�ʽ������,�����ϱ���
    
    ###!!!Ŀǰ���ڱ������в���:�����ֶ���ProgID��Ҫ��
    han_py_dict = {}
    
    c_list = pyIO.read_file_content(path)
    #print 'c_list= ', len(c_list)
    #print 'path= ', path
    
    t = '\n'.join(c_list).encode('utf8')
    t = t.replace(b'encoding="GBK"', b'encoding="utf-8"')

    root = ET.fromstring(t)
    for child in root[1:]:
        han = ''
        result_list = []
        for elem in child.iterfind('Word'):
            if elem.text is not None:
                han = elem.text
                han_py_dict[han] = []
        for elem in child.iterfind('Pronunciation/PinYin'):
            if elem.text is not None:
                han_py_dict[han].append(elem.text)

    return han_py_dict

def get_zhs_zht_han2pinyin_dict():
    ###����ƴ��
    path = '/Users/daiqiang/speech_synthesis_svr_proj/document/data/dict/max_GB2312-6763.xml'
    zh_chs_dict = get_han2py_dict(path)
    path = '/Users/daiqiang/speech_synthesis_svr_proj/document/data/dict/max_GB2312-6763_fanti.xml'
    zh_cht_dict = get_han2py_dict(path)
    logging.info('len(zh_chs_dict)= %s'%len(zh_chs_dict))
    logging.info('len(zh_cht_dict)= %s'%len(zh_cht_dict))
    
#     ###����Ƿ��ظ�:���������ظ���,ֱ�Ӻ���
#     for k,v in zh_chs_dict.items():
#         if k in zh_cht_dict:
#             print get_cur_info(), 'error!'
#             print k, v
#             sys.exit(0)

    ###�ϲ�ƴ��dict
    zh_py_dict = zh_cht_dict
    zh_py_dict.update(zh_chs_dict)
    logging.info('len(zh_py_dict)= %s'%len(zh_py_dict))
    return zh_py_dict


###����Ϊ����-->ƴ����xml; ��������������,���Ը�ʽ��:[(han, pinyin_list), (han, pinyin_list),]
def save2WordPinyinXml(file_name, file_description, word_pinyin_list):
    ###����xml�ļ�
    a = ET.Element('Dictionary')
    
    b = ET.SubElement(a, 'DictionaryHeader')
    c = ET.SubElement(b, 'DictionaryLanguage')
    c.text = 'zh-cn'
    d = ET.SubElement(b, 'DictionaryName')
    d.text = file_description
    
    for index,py_list in enumerate(word_pinyin_list):
        w = py_list[0]###.lower()
        b = ET.SubElement(a, 'DictionaryEntry')
        c = ET.SubElement(b, 'Word')
        c.text = w
        for i,py in enumerate(py_list[1]):
            print(index, py_list, py)
            d = ET.SubElement(b, 'Pronunciation')
            e = ET.SubElement(d, 'ProID')
            e.text = '%s'%(i+1)
            
            f = ET.SubElement(d, 'PartOfSpeech')
            f.text = ' '
            
            g = ET.SubElement(d, 'PinYin')
            py = changeDoubleSpace2SingleSpace(py)
            py = removeHeadTailSpace(py)
            g.text = py
            
            h = ET.SubElement(d, 'BianDiao')
            h.text = ' '

#     PrintObjectInfo(ET)
    text = ET.tostring(a, encoding="gbk", method="xml")
    text = text.decode('gbk')
#     text = text.decode('gbk')
#     print (type(text))
#     print (text[:1000])
#     tree = ET.ElementTree(a)
#     f = open(file_name, 'rb+')
#     tree.write(f)
#     f.close()
#     tree.write(sys.stdout)
    
    text = text.replace('encoding=\'gbk\'', 'encoding="GBK"')

    text = text.replace('<DictionaryHeader>', '\n<DictionaryHeader>')
    text = text.replace('</DictionaryHeader>', '</DictionaryHeader>\n')
    text = text.replace('</DictionaryEntry>', '</DictionaryEntry>\n')
    
# 
    ###���ڶ���˿ո�,Ŀǰ��֪����ô���ȽϺ�,����ȥ��
    text = text.replace('<PartOfSpeech> </PartOfSpeech>', '<PartOfSpeech></PartOfSpeech>')
    text = text.replace('<BianDiao> </BianDiao>', '<BianDiao></BianDiao>')
    ###���ﲹ��ո�
    text = text.replace('<DictionaryHeader>', '  <DictionaryHeader>')
    text = text.replace('<DictionaryEntry>',  '  <DictionaryEntry>')

    clear_to_file(file_name)
#     add_to_file(file_name, '<?xml version="1.0" encoding="GBK"?>')
    add_to_file(file_name, text)
#     f = open(file_name, 'wb+')
#     f.write(text)
#     f.close()
