'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
from com.zoho.crm.library.exception.Exception import ZCRMException
from com.zoho.crm.library.common.Utility import APIConstants
from com.zoho.crm.library.api.APIRequest import APIRequest

class APIHandler(object):
    '''
    This class is to wrap all the details required to make an api call(i.e. REQUEST_METHOD,REQUEST_URL,REQUEST_BODY,...etc)
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.requestUrlPath=None
        self.requestBody=None
        self.requestHeaders=None
        self.requestParams=None
        self.requestMethod=None
        self.requestAPIKey=None

class EntityAPIHandler(APIHandler):
    '''
    This class is to deal with all the entity single records
    '''
    def __init__(self,zcrmRecord):
        self.zcrmRecord=zcrmRecord
    
    def getRecord(self):
        try:
            handlerIns=APIHandler()
            handlerIns.requestUrlPath=self.zcrmRecord.moduleAPIName+"/"+str(self.zcrmRecord.entityID)
            handlerIns.requestMethod=APIConstants.REQUEST_METHOD_GET
            apiResponse=APIRequest(handlerIns).getAPIResponse()
            print apiResponse.responseJson
        except ZCRMException as ex:
            raise ex