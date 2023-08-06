'''
Created on Aug 16, 2017

@author: sumanth-3058
'''

class ZohoOAuthConstants(object):
    '''
    OAuth constants
    '''
    IAM_URL="iamURL";
    SCOPES="scope";
    STATE="state";
    STATE_OBTAINING_GRANT_TOKEN="OBTAIN_GRANT_TOKEN";
    RESPONSE_TYPE="response_type";
    RESPONSE_TYPE_CODE="code";
    CLIENT_ID="client_id";
    CLIENT_SECRET="client_secret";
    REDIRECT_URL="redirect_uri";
    ACCESS_TYPE="access_type";
    ACCESS_TYPE_OFFLINE="offline";
    ACCESS_TYPE_ONLINE="online";
    PROMPT="prompt";
    PROMPT_CONSENT="consent";
    GRANT_TYPE="grant_type";
    GRANT_TYPE_AUTH_CODE="authorization_code";
    
    GRANT_TYPE_REFRESH="refresh_token";
    CODE="code";
    GRANT_TOKEN="grant_token";
    ACCESS_TOKEN="access_token";
    REFRESH_TOKEN="refresh_token";
    EXPIRES_IN = "expires_in";
    EXPIRIY_TIME = "expiry_time";
    PERSISTENCE_HANDLER_CLASS = "persistence_handler_class";
    TOKEN = "token";
    DISPATCH_TO = "dispatchTo";
    OAUTH_TOKENS_PARAM = "oauth_tokens";
    
    OAUTH_HEADER_PREFIX="Zoho-oauthtoken ";
    AUTHORIZATION="Authorization";
    REQUEST_METHOD_GET="GET";
    REQUEST_METHOD_POST="POST";
    
    RESPONSECODE_OK=200;

class ZohoOAuthException(Exception):
    '''
    This is the custom exception class for handling Client Library OAuth related exceptions 
    '''
    def __init__(self, errMessage):
        self.message=errMessage
        Exception.__init__(self,errMessage)

    def __str__(self):
        return self.message

class ZohoOAuthHTTPConnector(object):
    '''
    This module is to make HTTP connections, trigger the requests and receive the response
    '''
    @staticmethod
    def getInstance(url,params=None,headers=None,body=None,method=None):
        return ZohoOAuthHTTPConnector(url,params,headers,body,method)
    
    def __init__(self, url,params,headers,body,method):
        '''
        Constructor
        '''
        self.url=url
        self.reqHeaders=headers
        self.reqMethod=method
        self.reqParams=params
        self.reqBody=body
        
    def triggerRequest(self):
        response=None
        import requests,json
        if(self.reqMethod == ZohoOAuthConstants.REQUEST_METHOD_GET):
            response=requests.get(self.url,params=self.reqParams, headers=self.reqHeaders,allow_redirects=False)
        elif(self.reqMethod==ZohoOAuthConstants.REQUEST_METHOD_POST):
            response=requests.post(self.url,data=json.dumps(self.reqBody), params=self.reqParams,headers=self.reqHeaders,allow_redirects=False)
        return response
    def setUrl(self,url):
        self.url=url
    def getUrl(self):
        return self.url
    def addHttpHeader(self,key,value):
        self.reqHeaders[key]=value
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
        self.reqParams[key]=value
    def getHttpRequestParams(self):
        return self.reqParams
    
class ZohoOAuthParams(object):
    '''
    This class is to OAuth related params(i.e. client_id,client_secret,..)
    '''
    def __init__(self, client_id,client_secret,redirect_uri):
        '''
        Constructor
        '''
        self.clientID=client_id
        self.clientSecret=client_secret
        self.redirectUri=redirect_uri
    @staticmethod
    def getInstance(client_id,client_secret,redirect_uri):
        return ZohoOAuthParams(client_id,client_secret,redirect_uri)
    
import logging
logger=logging.getLogger('Client_Library_OAUTH')
class Logger(object):
    '''
    This class is to log the exceptions onto console and file
    '''
    @staticmethod
    def addLog(message,level,exception=None):
        logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        
        fileHandler=logging.FileHandler("oauth.log")
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
        elif(level==logging.INFO):
            logger.info(message)
        elif(level==logging.WARNING):
            logger.warning(message)