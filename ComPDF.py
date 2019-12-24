# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 17:20:44 2019

@author: Administrator
"""

import os, sys, codecs
from argparse import ArgumentParser, RawTextHelpFormatter
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

def getfilenames(filepath='',filelist_out=[],file_ext='all'):
    # 遍历filepath下的所有文件，包括子目录下的文件
    for fpath, dirs, fs in os.walk(filepath):
        for f in fs:
            fi_d = os.path.join(fpath, f)
            if  file_ext == 'all':
                filelist_out.append(fi_d)
            elif os.path.splitext(fi_d)[1] == file_ext:
                filelist_out.append(fi_d)
            else:
                pass
    return filelist_out

def mergefiles(path, output_filename, import_bookmarks=False):
    # 遍历目录下的所有pdf将其合并输出到一个pdf文件中，输出的pdf文件默认带书签，书签名为之前的文件名
    # 默认情况下原始文件的书签不会导入，使用import_bookmarks=True可以将原文件所带的书签也导入到输出的pdf文件中
    merger = PdfFileMerger()
    filelist = getfilenames(filepath=path, file_ext='.pdf')
    if len(filelist) == 0:
        print("当前目录及子目录下不存在pdf文件")
        sys.exit()
    for filename in filelist:
        f = codecs.open(filename, 'rb')
        file_rd = PdfFileReader(f)
        short_filename = os.path.basename(os.path.splitext(filename)[0])
        if file_rd.isEncrypted == True:
            print('不支持的加密文件：%s'%(filename))
            continue
        merger.append(file_rd, bookmark=short_filename, import_bookmarks=import_bookmarks)
        print('合并文件：%s'%(filename))
        f.close()
    out_filename=os.path.join(os.path.abspath(path), output_filename)
    merger.write(out_filename)
    print('合并后的输出文件：%s'%(out_filename))
    merger.close()

path = "在这里填写pdf所在的地址"
output_filename = "填写输出文件名.pdf"
mergefiles(path, output_filename, import_bookmarks=False)