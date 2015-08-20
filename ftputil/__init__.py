__author__ = 'march'
__all__ = ['optionConfig','sftp','dotdict','linuxPath','setupLogging']

class dotdict(dict):
    '''
    dot.notation access to dictionary attributes
    >>> dotdict({'c':1,'d':2})
    {'c': 1, 'd': 2}
    '''
    def __getattr__(self, attr):
         return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

def linuxPath(pathName):
    '''
    >>> linuxPath('C:\Users\march\AppData\Local\Temp\svn57BE.tmp')
    'C:/Users/march/AppData/Local/Temp/svn57BE.tmp'
    '''
    return pathName.replace('\\','/')

def setupLogging(options):
    import logging
    LOGGING_LEVELS = {'critical': logging.CRITICAL,
                      'error': logging.ERROR,
                      'warning': logging.WARNING,
                      'info': logging.INFO,
                      'debug': logging.DEBUG}
    logging_level = LOGGING_LEVELS.get(options.logging_level, logging.NOTSET)
    logging.basicConfig(level=logging_level, filename=options.logging_file,
                      format='%(asctime)s %(levelname)s: %(message)s',
                          datefmt='%Y-%m-%d %H:%M:%S')

def setup_logging(default_path='logging.json', default_level=None,env_key='LOG_CFG'):
    """Setup logging configuration
    """
    import json
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

if __name__ == "__main__":
    import doctest
    doctest.testmod()