'''
Created on Jul 28, 2017

@author: sumanth-3058
'''
from com.zoho.crm.library.common.Utility import ZCRMConfigUtil, APIConstants,HTTPConnector
from com.zoho.crm.library.exception.Exception import ZCRMException
from com.zoho.crm.library.api.APIResponse import APIResponse, BulkAPIResponse
class APIRequest(object):
    '''
    This class is to wrap the API request related stuff like request params,headers,body,..etc
    '''
    def __init__(self, apiHandlerIns):
        '''
        Constructor
        '''
        self.constructAPIUrl()
        self.url+=apiHandlerIns.requestUrlPath
        if(not self.url.startswith("http")):
            self.url="https://"+self.url
        self.requestBody=apiHandlerIns.requestBody
        self.requestHeaders=apiHandlerIns.requestHeaders
        self.requestParams=apiHandlerIns.requestParams
        self.requestMethod=apiHandlerIns.requestMethod
        self.requestAPIKey=apiHandlerIns.requestAPIKey
    
    def constructAPIUrl(self):
        self.url=ZCRMConfigUtil.getAPIBaseUrl()+"/crm/"+ZCRMConfigUtil.getAPIVersion()+"/"
    
    def authenticateRequest(self):
        accessToken=ZCRMConfigUtil.getInstance().getAccessToken()
        if(self.requestHeaders==None):
            self.requestHeaders={APIConstants.AUTHORIZATION:APIConstants.OAUTH_HEADER_PREFIX+accessToken}
        else:
            self.requestHeaders[APIConstants.AUTHORIZATION]=APIConstants.OAUTH_HEADER_PREFIX+accessToken
            
    def getAPIResponse(self):
        try:
            self.authenticateRequest()
            connector=HTTPConnector.getInstance(self.url, self.requestParams, self.requestHeaders, self.requestBody, self.requestMethod, self.requestAPIKey, False)
            response=connector.triggerRequest()
            return APIResponse(response,response.status_code,self.url,self.requestAPIKey)
        except ZCRMException as ex:
            raise ex
    def getBulkAPIResponse(self):
        try:
            self.authenticateRequest()
            connector=HTTPConnector.getInstance(self.url, self.requestParams, self.requestHeaders, self.requestBody, self.requestMethod, self.requestAPIKey, False)
            response=connector.triggerRequest()
            return BulkAPIResponse(response,response.status_code,self.url,self.requestAPIKey)
        except ZCRMException as ex:
            raise ex
            
            
        