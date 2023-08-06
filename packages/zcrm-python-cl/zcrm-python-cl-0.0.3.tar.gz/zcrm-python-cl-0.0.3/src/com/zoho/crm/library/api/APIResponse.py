'''
Created on Aug 1, 2017

@author: sumanth-3058
'''
from com.zoho.crm.library.exception.Exception import ZCRMException
from com.zoho.crm.library.common.Utility import APIConstants

class CommonAPIResponse(object):
    def __init__(self,response,statusCode,url,apiKey=None):
        '''
        Constructor
        '''
        self.response=response
        self.statusCode=statusCode
        self.apiKey=apiKey
        self.url=url
        self.setResponseJson()
        self.processResponse()
    '''
    def getStatusCode(self):
        return self.statusCode
    def getResponseJson(self):
        return self.responseJson
    def getResponse(self):
        return self.response
    def getAPIName(self):
        return self.apiName
    def getResponseHeaders(self):
        return self.responseHeaders
    def setMessage(self,message):
        self.responseMessage=message
    def getMessage(self):
        return self.responseMessage
    def setDetails(self,details):
        self.responseDetails=details
    def getDetails(self):
        return self.responseDetails
    '''
    def setResponseJson(self):
        self.responseJson=self.response.json()
        self.responseHeaders=self.response.headers
    def processResponse(self):
        if(self.statusCode in APIConstants.FAULTY_RESPONSE_CODES):
            self.handleFaultyResponses()
        else:
            self.processResponseData()
    
    def handleFaultyResponses(self):
        return
    def processResponseData(self):
        return
class APIResponse(CommonAPIResponse):
    '''
    classdocs
    '''
    def __init__(self, response,statusCode,url,apiKey):
        '''
        Constructor
        '''
        super(APIResponse,self).__init__(response,statusCode,url,apiKey)
    def handleFaultyResponses(self):
        if(self.statusCode==APIConstants.RESPONSECODE_NO_CONTENT):
            errorMsg=APIConstants.INVALID_DATA+"-"+APIConstants.INVALID_ID_MSG
            exception=ZCRMException(self.url,self.statusCode,errorMsg,APIConstants.NO_CONTENT,None,errorMsg)
            raise exception
        else:
            responseJSON=self.responseJson
            exception=ZCRMException(self.url,self.statusCode,responseJSON[APIConstants.MESSAGE],responseJSON[APIConstants.CODE],responseJSON[APIConstants.DETAILS],responseJSON[APIConstants.MESSAGE])
            raise exception
    def processResponseData(self):
        respJson=self.responseJson
        if(self.apiKey in respJson):
            respJson=self.responseJson[self.apiKey]
            if(isinstance(respJson, list)):
                respJson=respJson[0]
        if(APIConstants.STATUS in respJson and (respJson[APIConstants.STATUS]==APIConstants.STATUS_ERROR)):
            exception=ZCRMException(self.url,self.statusCode,respJson[APIConstants.MESSAGE],respJson[APIConstants.CODE],respJson[APIConstants.DETAILS],respJson[APIConstants.MESSAGE])
            raise exception
        elif(APIConstants.STATUS in respJson and (respJson[APIConstants.STATUS]==APIConstants.STATUS_SUCCESS)):
            self.status=respJson[APIConstants.STATUS]
            self.code=respJson[APIConstants.CODE]
            self.message=respJson[APIConstants.MESSAGE]
            self.details=respJson[APIConstants.DETAILS]
        
class BulkAPIResponse(CommonAPIResponse):
    '''
    This class is to store the Bulk APIs responses
    '''
    def __init__(self, response,statusCode,url,apiKey):
        '''
        Constructor
        '''
        super(BulkAPIResponse,self).__init__(response,statusCode,url,apiKey)
        
    def handleFaultyResponses(self):
        if(self.statusCode==APIConstants.RESPONSECODE_NO_CONTENT):
            errorMsg=APIConstants.INVALID_DATA+"-"+APIConstants.INVALID_ID_MSG
            exception=ZCRMException(self.url,self.statusCode,errorMsg,APIConstants.NO_CONTENT,None,errorMsg)
            raise exception
        else:
            responseJSON=self.responseJson
            exception=ZCRMException(self.url,self.statusCode,responseJSON['message'],responseJSON['code'],responseJSON['details'],responseJSON['message'])
            raise exception
    def processResponseData(self):
        if(APIConstants.DATA in self.responseJson):
            dataList=self.responseJson[APIConstants.DATA]
            self.bulkEntityResponse=[]
            for eachRecord in dataList:
                if(APIConstants.STATUS in eachRecord):
                    self.bulkEntityResponse.append(EntityResponse(eachRecord))
            
class EntityResponse(object):
    '''
    This class is to store each entity response of the Bulk APIs response
    '''
    def __init__(self,entityResponse):
        '''
        Constructor
        '''
        self.responseJson=entityResponse
        self.code=entityResponse[APIConstants.CODE]
        self.message=entityResponse[APIConstants.MESSAGE]
        self.status=entityResponse[APIConstants.STATUS]
        if(APIConstants.DETAILS in entityResponse):
            self.details=entityResponse[APIConstants.DETAILS]
        if(APIConstants.ACTION in entityResponse):
            self.upsertAction=entityResponse[APIConstants.ACTION]
        if(APIConstants.DUPLICATE_FIELD in entityResponse):
            self.upsertDuplicateField=entityResponse[APIConstants.DUPLICATE_FIELD]
    @staticmethod
    def getInstance(self,entityResponse):
        return EntityResponse(entityResponse)