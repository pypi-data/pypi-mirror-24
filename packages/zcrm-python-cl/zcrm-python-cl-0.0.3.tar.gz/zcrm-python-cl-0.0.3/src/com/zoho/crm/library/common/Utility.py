'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
import requests
import json
from com.zoho.oauth.client.OAuthClient import ZohoOAuth
from com.zoho.crm.library.exception.Exception import ZCRMException

class HTTPConnector(object):
    '''
    This module is to make HTTP connections, trigger the requests and receive the response
    '''
    @staticmethod
    def getInstance(url,params,headers,body,method,apiKey,isBulkReq):
        return HTTPConnector(url,params,headers,body,method,apiKey,isBulkReq)
    
    def __init__(self, url,params,headers,body,method,apiKey,isBulkReq):
        '''
        Constructor
        '''
        self.url=url
        self.reqHeaders=headers
        self.reqMethod=method
        self.reqParams=params
        self.reqBody=body
        self.apiKey=apiKey
        self.isBulkReq=isBulkReq
        
    def triggerRequest(self):
        response=None
        if(self.reqMethod == APIConstants.REQUEST_METHOD_GET):
            #if(self.reqParams!=None and self.reqParams.length>0):
            #   self.url=self.url+'?'+self.getRequestParamsAsString(self.reqParams)
            response=requests.get(self.url, headers=self.reqHeaders,params=self.reqParams,allow_redirects=False)
        elif(self.reqMethod==APIConstants.REQUEST_METHOD_PUT):
            response=requests.put(self.url, data=self.reqBody,params=self.reqParams,headers=self.reqHeaders,allow_redirects=False)
        elif(self.reqMethod==APIConstants.REQUEST_METHOD_POST):
            response=requests.post(self.url,data=json.dumps(self.reqBody), params=self.reqParams,headers=self.reqHeaders,allow_redirects=False)
            #print response
            #print response.status_code
            #print response.json()
            #print response.content
            #obj=BulkAPIResponse(response,response.status_code,self.url,self.apiKey)
            #print obj.statusCode
            #print obj.bulkEntityResponse[0].message
            #print obj.bulkEntityResponse[0].code
            #print obj.bulkEntityResponse[0].status
            #print obj.bulkEntityResponse[0].details
        elif(self.reqMethod==APIConstants.REQUEST_METHOD_DELETE):
            response=requests.delete(self.url,headers=self.reqHeaders,params=self.reqParams,allow_redirects=False)
        return response
    def getRequestParamsAsString(self,params):
        mapAsString=''
        for key in params:
            mapAsString+=key+'='+params[key]
        return mapAsString
    def setUrl(self,url):
        self.url=url
    def getUrl(self):
        return self.url
    def addHttpHeader(self,key,value):
        self.reqHeaders.put(key,value)
    def getHttpHeaders(self):
        return self.reqHeaders
    def setHttpRequestMethod(self,method):
        self.reqMethod=method
    def getHttpRequestMethod(self):
        return self.reqMethod
    def setRequestBody(self,reqBody):
        self.reqBody=reqBody
    def getRequestBody(self):
        return self.reqBody
    def addHttpRequestParams(self,key,value):
        self.reqParams.put(key,value)
    def getHttpRequestParams(self):
        return self.reqParams

class APIConstants(object):
    '''
    This module holds the constants required for the client library
    '''
    ERROR="error"
    REQUEST_METHOD_GET="GET"
    REQUEST_METHOD_POST="POST"
    REQUEST_METHOD_PUT="PUT"
    REQUEST_METHOD_DELETE="DELETE"
    
    OAUTH_HEADER_PREFIX="Zoho-oauthtoken "
    AUTHORIZATION="Authorization"
    
    API_NAME="api_name"
    INVALID_ID_MSG = "The given id seems to be invalid."
    API_MAX_RECORDS_MSG = "Cannot process more than 100 records at a time."
    INVALID_DATA="INVALID_DATA"
    
    CODE_SUCCESS = "SUCCESS"
    
    STATUS_SUCCESS = "success"
    STATUS_ERROR = "error"
    
    LEADS = "Leads"
    ACCOUNTS = "Accounts"
    CONTACTS = "Contacts"
    DEALS = "Deals"
    QUOTES = "Quotes"
    SALESORDERS = "SalesOrders"
    INVOICES = "Invoices"
    PURCHASEORDERS = "PurchaseOrders"
    
    PER_PAGE = "per_page"
    PAGE = "page"
    COUNT = "count"
    MORE_RECORDS = "more_records"
    
    MESSAGE = "message"
    CODE = "code"
    STATUS = "status"
    DETAILS="details"
    
    DATA = "data"
    INFO = "info"
    
    RESPONSECODE_OK=200
    RESPONSECODE_CREATED=201
    RESPONSECODE_ACCEPTED=202
    RESPONSECODE_NO_CONTENT=204
    RESPONSECODE_MOVED_PERMANENTLY=301
    RESPONSECODE_MOVED_TEMPORARILY=302
    RESPONSECODE_NOT_MODIFIED=304
    RESPONSECODE_BAD_REQUEST=400
    RESPONSECODE_AUTHORIZATION_ERROR=401
    RESPONSECODE_FORBIDDEN=403
    RESPONSECODE_NOT_FOUND=404
    RESPONSECODE_METHOD_NOT_ALLOWED=405
    RESPONSECODE_REQUEST_ENTITY_TOO_LARGE=413
    RESPONSECODE_UNSUPPORTED_MEDIA_TYPE=415
    RESPONSECODE_TOO_MANY_REQUEST=429
    RESPONSECODE_INTERNAL_SERVER_ERROR=500
    
    DOWNLOAD_FILE_PATH="../../../../../../resources"
    
    USER_EMAIL_ID="user_email_id"
    ACTION="action"
    DUPLICATE_FIELD="duplicate_field"
    NO_CONTENT="No Content"
    FAULTY_RESPONSE_CODES=[RESPONSECODE_NO_CONTENT,RESPONSECODE_NOT_FOUND,RESPONSECODE_AUTHORIZATION_ERROR,RESPONSECODE_BAD_REQUEST,RESPONSECODE_FORBIDDEN,RESPONSECODE_INTERNAL_SERVER_ERROR,RESPONSECODE_METHOD_NOT_ALLOWED,RESPONSECODE_MOVED_PERMANENTLY,RESPONSECODE_MOVED_TEMPORARILY,RESPONSECODE_REQUEST_ENTITY_TOO_LARGE,RESPONSECODE_TOO_MANY_REQUEST,RESPONSECODE_UNSUPPORTED_MEDIA_TYPE]
    
class ZCRMConfigUtil(object):
    '''
    This class is to deal with configuration related things
    '''
    configPropDict={}
    @staticmethod
    def getInstance():
        return ZCRMConfigUtil()
    @staticmethod
    def initialize(isToInitializeOAuth):
        from com.PathIdentifier import PathIdentifier
        import os
        dirSplit=os.path.split(PathIdentifier.getClientLibraryRoot())
        resources_path = os.path.join(dirSplit[0],'resources','configuration.properties')
        filePointer=open(resources_path,"r")
        ZCRMConfigUtil.configPropDict=CommonUtil.getFileContentAsDictionary(filePointer)
        if(isToInitializeOAuth):
            ZohoOAuth.initialize()
    @staticmethod
    def getAPIBaseUrl():
        return ZCRMConfigUtil.configPropDict["apiBaseUrl"]
    @staticmethod
    def getAPIVersion():
        return ZCRMConfigUtil.configPropDict["apiVersion"]
    def getAccessToken(self):
        from com.zoho.crm.library.setup.ZCRMRestClient import ZCRMRestClient
        userEmail=ZCRMRestClient.getInstance().getCurrentUserEmailID()
        if(userEmail==None and ZCRMConfigUtil.configPropDict['currentUserEmail']==None):
            raise ZCRMException('fetching current user email',400,'Current user should either be set in ZCRMRestClient or in configuration.properties file')
        elif(userEmail==None):
            userEmail=ZCRMConfigUtil.configPropDict['currentUserEmail']
        clientIns=ZohoOAuth.getClientInstance()
        clientIns.getAccessToken(userEmail)
        
class CommonUtil(object):
    '''
    This class is to provide utility methods
    '''
    @staticmethod
    def getFileContentAsDictionary(filePointer) :
        dictionary={}
        for line in filePointer:
            line=line.rstrip()
            keyValue=line.split("=")
            if(not keyValue[0].startswith('#')):
                dictionary[keyValue[0]]=keyValue[1]
        filePointer.close()
        return dictionary
        