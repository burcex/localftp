import sys,os,logging
import ConfigParser
from ftputil import dotdict

def __infoConfig(filename):
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.readfp(open(filename))
        sftpServer = dotdict(cfg.items('sftpServer'))
        pathInfo = dotdict(cfg.items('pathInfo'))
    except IOError , e:
        print e  
    return (sftpServer,pathInfo)

def main():
    filename = 'info.ini'
    filename = os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), filename))
    logging.info(filename)
    return __infoConfig(filename)
