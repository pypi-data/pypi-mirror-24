'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
import threading
from com.zoho.crm.library.common.Utility import ZCRMConfigUtil

class ZCRMRestClient(object):
    '''
    classdocs
    '''
    @staticmethod
    def getInstance():
        return ZCRMRestClient()

    def getCurrentUserEmailID(self):
        #print threading.local.__dict__
        print threading.current_thread.__dict__
        print threading.currentThread().__getattribute__('email')
        return (threading.local()).userEmail
    
    @staticmethod
    def initialize():
        ZCRMConfigUtil.initialize(True)