import paramiko
from ftputil import linuxPath
import logging
import os

class sftp():

    def __init__(self,sftpServer,pathInfo,commitedFileName):
        self.sftp = sftpServer
        self.paths = pathInfo
        self.commitedFileName = commitedFileName

    def connect(self):
        self.transport = paramiko.Transport((self.sftp.host, int(self.sftp.port)))
        self.transport.connect(username = self.sftp.username, password = self.sftp.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def dealCommitFile(self):
        localList=[]
        remotepaths = self.paths.remotepaths.split(',')
        localSvnPath = self.paths.localsvnpath
        commitedFileName = self.commitedFileName

        remoteList = [[] for i in remotepaths]
        with open(commitedFileName) as localPaths:
            for rawLocalPath in localPaths: 
                localPath = linuxPath(rawLocalPath)
                localList.append(localPath.strip())
                for idx,remotePath in enumerate(remotepaths):
                    remoteList[idx].append(localPath.replace(localSvnPath,remotePath).strip())
        return (localList,remoteList)

    #
    def putFile(self,localList,remoteList):
        remotepaths = self.paths.remotepaths.split(',')
        for reIdx,remotePath in enumerate(remotepaths):
            for locIdx,val in enumerate(localList):
                logging.info(val+'==>'+remoteList[reIdx][locIdx])
                if logging.getLogger().getEffectiveLevel() == 0 :
                    self.sftp.put(val, remoteList[reIdx][locIdx])

    def dealUploadFiles(self):
        commitedFileName = self.commitedFileName
        localSvnPath = self.paths.localsvnpath
        with open(commitedFileName,'r') as read:
            upploadFiles = [line.replace('\\','/').replace(localSvnPath,'.') for line in read.readlines()]
        return upploadFiles

    def mergeFilesListInremoteFile(self,upploadFiles):
        rsyncfilelist = self.paths.rsyncfilelist

        with self.sftp.file(rsyncfilelist,'ra') as remoteFile:
            if logging.getLogger().getEffectiveLevel() == 0 :
                if remoteFile.readline() != '':
                    remoteFile.write('\n')
                remoteFile.writelines(upploadFiles)

    def close(self):
        self.sftp.close()
        self.transport.close()