#!/usr/local/python33/bin/python3
#-*- coding: gb18030 -*-

import sys
import os

# if not isPlatform3():
#     ###��Ҫ��װwindows�µ�pdfminer�⣬mac��û��
#     from pdfminer.pdfparser import PDFParser, PDFDocument  
#     from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter  
#     from pdfminer.pdfdevice import PDFDevice  
#     from pdfminer.converter import PDFPageAggregator  
#     from pdfminer.layout import *

def getPdfPages(pdf_name):
    fp = open(pdf_name, 'rb')
    #���ļ�����������һ��pdf�ĵ�������  
    parser = PDFParser(fp)  
    # ����һ��  PDF �ĵ�   
    doc = PDFDocument()  
    # ���ӷ����� ���ĵ�����  
    parser.set_document(doc)  
    doc.set_parser(parser)  
    
    # �ṩ��ʼ������  
    # ���û������ �ʹ���һ���յ��ַ���  
    doc.initialize()  
    # ����ĵ��Ƿ��ṩtxtת�������ṩ�ͺ���  
    if not doc.is_extractable:  
        #raise PDFTextExtractionNotAllowed  
        logging.info('=========not txt change %s'%pdf_name)
        return False

    logging.info('-----processing: %s'%pdf_name)
    # ����PDf ��Դ������ ����������Դ  
    rsrcmgr = PDFResourceManager()  
    # ����һ��PDF�豸����  
    laparams = LAParams()  
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)  
    interpreter = PDFPageInterpreter(rsrcmgr, device)  
    # �����ĵ�������ÿһҳ������  
    # doc.get_pages() ��ȡpage�б�  
    # ѭ�������б�ÿ�δ���һ��page������  
    # ����layout��һ��LTPage���� �������� ���page�������ĸ��ֶ��� һ�����
    ###LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal �ȵ� ��Ҫ��ȡ�ı��ͻ�ö����text���ԣ�
    pages = doc.get_pages()  
    return pages
        
def isPdfValid(pdf_name):
    if pdf_name[-4:].lower() != '.pdf':
        logging.info('-------------------not pdf file: %s'%pdf_name)
        return False
        
    try:
        getPdfPages(pdf_name)
    except:
        return False
        pass###��������
    return True

###ע��:�����Ƕ��������,��ʹ�ҵ���Ҳû�й�ϵ     
def parsePdfFile(pdf_name):
    all_text = ''
    if pdf_name[-4:].lower() != '.pdf':
        logging.info('-------------------not pdf file:%s'%pdf_name)
        return all_text

    #try:
    if True:
        pdf_pages = getPdfPages(pdf_name)
        for i, page in enumerate(pdf_pages):  
            interpreter.process_page(page)  
            layout = device.get_result()  
            for x in layout:  
                if isinstance(x, LTTextBox) or isinstance(x, LTTextLine):
                    all_text += x.get_text()
                    all_text += ' '
        fp.close()
        device.close()
#     except:
#         print 'error happens somewhere!'
#         pass###��������
#     print 'all_text len= ',len(all_text)

    return all_text

