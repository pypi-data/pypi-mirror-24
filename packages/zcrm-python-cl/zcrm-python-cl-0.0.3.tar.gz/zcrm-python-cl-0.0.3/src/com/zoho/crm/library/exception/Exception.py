'''
Created on Aug 16, 2017

@author: sumanth-3058
'''

class ZCRMException(Exception):
    '''
    This is the custom exception class for handling for Client Library exceptions 
    '''
    message = 'Error occurred for {url}. Error Code: {code} Response content: {content}'

    def __init__(self, url, status, errMessage,exceptionCode,details=None,content=None):
        self.url = url
        self.statusCode = status
        self.content = content
        self.errorMessage=errMessage
        self.exceptionCode=exceptionCode
        self.exceptionDetails=details
        Exception.__init__(self,status)

    def __str__(self):
        return self.message.format(url=self.url,code=self.statusCode,content=self.content)

import logging
logger=logging.getLogger('Client_Library')    
class Logger(object):
    '''
    This class is to log the exceptions onto console
    '''
    @staticmethod
    def addLog(message,level=None,exception=None):
        logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        
        fileHandler=logging.FileHandler("client_library.log")
        fileHandler.setLevel(logging.DEBUG)
        
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        consoleHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(consoleHandler)
        logger.addHandler(fileHandler)
        
        if(exception!=None):
            message+='; Exception Message::'+exception.__str__()
        if(level==logging.ERROR):
            logger.error(message)
        elif(level==logging.INFO or level==logging.DEBUG):
            logger.debug(message)
        elif(level==logging.WARNING):
            logger.warning(message)
