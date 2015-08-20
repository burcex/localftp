#!/usr/bin/env python
# -*- coding:utf-8 -*- 

#import pdb
import sys,os
import optparse
import codecs
from ftputil import *
import logging

def main():
    #pdb.set_trace()

    commitedFilesList=sys.argv[1]
    logging.info(commitedFilesList)
    commitedFileName = linuxPath(commitedFilesList)
    logging.info(commitedFileName)

    sftpServer, pathInfo = optionConfig.main()

    sftpObj = sftp.sftp(sftpServer,pathInfo,commitedFileName)
    logging.warn('sftp登陆')
    sftpObj.connect()

    logging.warn('整理上传文件')
    localList,remoteList = sftpObj.dealCommitFile()
    logging.info(remoteList)

    # sftp 传输文件
    logging.warn('sftp传输开始')
    fileList = (localList,remoteList)
    sftpObj.putFile(*fileList)

    # sftp 处理上传文件
    upploadFiles = sftpObj.dealUploadFiles()
    logging.warn(upploadFiles)
    # sftp 结束
    logging.warn('生成上传文件列表')
    sftpObj.mergeFilesListInremoteFile(upploadFiles)

    # sftp 结束
    sftpObj.close()

    print 'Upload done.'
if __name__ == '__main__':

    outEncoding = sys.stdout.encoding
    sys.stdout = codecs.getwriter(outEncoding)(sys.stdout)

    if len(sys.argv) == 1:
       raise SystemExit('Specify at least 1 argument')

    parser = optparse.OptionParser()
    parser.add_option('-l', '--logging-level', help='Logging level')
    parser.add_option('-f', '--logging-file', help='Logging file name')
    (options, args) = parser.parse_args()
    
    setupLogging(options)
    main()