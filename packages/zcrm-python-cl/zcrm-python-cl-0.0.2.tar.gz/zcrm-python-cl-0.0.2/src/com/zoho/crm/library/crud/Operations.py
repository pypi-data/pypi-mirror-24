'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
from com.zoho.crm.library.api.APIHandler import EntityAPIHandler

class ZCRMModule(object):
    '''
    This class is to deal with Zoho CRM modules
    '''
    def __init__(self, moduleAPIName):
        '''
        Constructor
        '''
        self.moduleAPIName=moduleAPIName
    
    @staticmethod
    def getInstance(moduleAPIName):
        return ZCRMModule(moduleAPIName)
    def getRecord(self,entityID):
        record=ZCRMRecord.getInstance(self.moduleAPIName, entityID)
        return EntityAPIHandler(record).getRecord()

class ZCRMRecord(object):
    '''
    This class is to deal with Zoho CRM entity records
    '''
    def __init__(self,moduleAPIName,entityID):
        '''
        Constructor
        '''
        self.moduleAPIName=moduleAPIName
        self.entityID=entityID
    @staticmethod
    def getInstance(moduleAPIName,entityID):
        return ZCRMRecord(moduleAPIName,entityID)