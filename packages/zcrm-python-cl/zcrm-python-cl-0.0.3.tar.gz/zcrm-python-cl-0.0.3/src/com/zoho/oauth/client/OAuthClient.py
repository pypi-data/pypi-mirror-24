'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
from com.zoho.oauth.common.Utility import Logger,ZohoOAuthConstants,ZohoOAuthException,ZohoOAuthHTTPConnector,\
    ZohoOAuthParams
from com.zoho.oauth.clientapp.Persistence import ZohoOAuthPersistenceHandler
class ZohoOAuth(object):
    '''
    This class is to load oauth configurations and provide OAuth request URIs
    '''
    configProperties={}
    iamURL='https://accounts.localzoho.com'
    
    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod
    def initialize():
        try:
            from PathIdentifier import PathIdentifier
            import os
            resources_path = os.path.join(PathIdentifier.getClientLibraryRoot(),'resources','oauth_configuration.properties')
            filePointer=open(resources_path,"r")
            ZohoOAuth.configProperties=ZohoOAuth.getFileContentAsDictionary(filePointer)
            oAuthParams=ZohoOAuthParams.getInstance(ZohoOAuth.configProperties[ZohoOAuthConstants.CLIENT_ID], ZohoOAuth.configProperties[ZohoOAuthConstants.CLIENT_SECRET], ZohoOAuth.configProperties[ZohoOAuthConstants.REDIRECT_URL])
            ZohoOAuthClient.getInstance(oAuthParams)
        except Exception as ex:
            import logging
            Logger.addLog('Exception occured while reading oauth configurations',logging.ERROR,ex)
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
    @staticmethod
    def getGrantURL():
        return (ZohoOAuth.iamURL+"/oauth/v2/auth")
    @staticmethod
    def getTokenURL():
        return (ZohoOAuth.iamURL+"/oauth/v2/token")
    @staticmethod
    def getRefreshTokenURL():
        return (ZohoOAuth.iamURL+"/oauth/v2/token")
    @staticmethod
    def getRevokeTokenURL():
        return (ZohoOAuth.iamURL+"/oauth/v2/token/revoke")
    @staticmethod
    def getUserInfoURL():
        return (ZohoOAuth.iamURL+"/oauth/user/info")
    @staticmethod
    def getClientInstance():
        oAuthClientIns=ZohoOAuthClient.getInstance()
        if(oAuthClientIns==None):
            raise ZohoOAuthException('ZohoOAuth.initialize() must be called before this')
        return oAuthClientIns

class ZohoOAuthClient(object):
    '''
    This class is to generate oauth related tokens
    '''
    oAuthParams=None
    oAuthClientIns=None

    def __init__(self, oauthParams):
        '''
        Constructor
        '''
        ZohoOAuthClient.oAuthParams=oauthParams
        
    @staticmethod
    def getInstance(param=None):
        if(param!=None and ZohoOAuthClient.oAuthClientIns==None):
            ZohoOAuthClient.oAuthClientIns=ZohoOAuthClient(param)
        return ZohoOAuthClient.oAuthClientIns
            
    def getAccessToken(self,userEmail):
        try:
            handler=ZohoOAuthPersistenceHandler()
            oAuthTokens=handler.getOAuthTokens(userEmail)
            try:
                return oAuthTokens.accessToken
            except Exception as e:
                import logging
                Logger.addLog("Access token expired hence refreshing",logging.INFO,e)
                oAuthTokens=self.refreshAccessToken(oAuthTokens.refreshToken,userEmail)
                return oAuthTokens.accessToken
        except Exception as ex:
            Logger.addLog("Exception occured while fetching oauthtoken from db",logging.ERROR,ex)
    def refreshAccessToken(self,refreshToken,userEmail):
        if(refreshToken==None):
            raise ZohoOAuthException("Refresh token not provided!")
        try:
            connector=self.getConnector(ZohoOAuth.getRefreshTokenURL())
            connector.addHttpRequestParams(ZohoOAuthConstants.GRANT_TYPE,ZohoOAuthConstants.GRANT_TYPE_REFRESH)
            connector.addHttpRequestParams(ZohoOAuthConstants.REFRESH_TOKEN,refreshToken)
            connector.setHttpRequestMethod(ZohoOAuthConstants.REQUEST_METHOD_POST)
            response=connector.triggerRequest()
            responseJSON=response.json()
            if(ZohoOAuthConstants.ACCESS_TOKEN in responseJSON):
                oAuthTokens=self.getTokensFromJson(responseJSON)
                oAuthTokens.setUserEmail(userEmail)
                ZohoOAuthPersistenceHandler().saveOAuthTokens(oAuthTokens)
            
        except ZohoOAuthException as ex:
            import logging
            Logger.addLog("Exception occured while refreshing oauthtoken",logging.ERROR,ex)
            
    def generateAccessToken(self,grantToken):
        if(grantToken==None):
            raise ZohoOAuthException("Grant token not provided!")
        try:
            connector=self.getConnector(ZohoOAuth.getTokenURL())
            connector.addHttpRequestParams(ZohoOAuthConstants.GRANT_TYPE,ZohoOAuthConstants.GRANT_TYPE_AUTH_CODE)
            connector.addHttpRequestParams(ZohoOAuthConstants.CODE,grantToken)
            connector.setHttpRequestMethod(ZohoOAuthConstants.REQUEST_METHOD_POST)
            print connector.reqParams
            response=connector.triggerRequest()
            responseJSON=response.json()
            if(ZohoOAuthConstants.ACCESS_TOKEN in responseJSON):
                oAuthTokens=self.getTokensFromJson(responseJSON)
                oAuthTokens.setUserEmail(self.getUserEmailFromIAM(oAuthTokens.accessToken))
                print oAuthTokens
                ZohoOAuthPersistenceHandler().saveOAuthTokens(oAuthTokens)
                return oAuthTokens
            else:
                raise ZohoOAuthException("Exception occured while fetching accesstoken from Grant Token;Response is:"+response.content)
            
        except ZohoOAuthException as ex:
            import logging
            Logger.addLog("Exception occured while generating access token",logging.ERROR,ex)
    
    def getTokensFromJson(self,responseJson):
        expiresIn = responseJson[ZohoOAuthConstants.EXPIRES_IN]
        expiresIn=expiresIn+(ZohoOAuthTokens.getCurrentTimeInMillis())
        accessToken=responseJson[ZohoOAuthConstants.ACCESS_TOKEN]
        refreshToken=None
        if(ZohoOAuthConstants.REFRESH_TOKEN in responseJson):
            refreshToken=responseJson[ZohoOAuthConstants.REFRESH_TOKEN]
        oAuthTokens = ZohoOAuthTokens(refreshToken,accessToken,expiresIn)
        return oAuthTokens;
    def getConnector(self,url):
        connector=ZohoOAuthHTTPConnector.getInstance(url,{})
        connector.addHttpRequestParams(ZohoOAuthConstants.CLIENT_ID, ZohoOAuthClient.oAuthParams.clientID)
        connector.addHttpRequestParams(ZohoOAuthConstants.CLIENT_SECRET, ZohoOAuthClient.oAuthParams.clientSecret)
        connector.addHttpRequestParams(ZohoOAuthConstants.REDIRECT_URL, ZohoOAuthClient.oAuthParams.redirectUri)
        return connector
    def getUserEmailFromIAM(self,accessToken):
        header={ZohoOAuthConstants.AUTHORIZATION:(ZohoOAuthConstants.OAUTH_HEADER_PREFIX+accessToken)}
        connector=ZohoOAuthHTTPConnector.getInstance(ZohoOAuth.getUserInfoURL(),None,header,None,ZohoOAuthConstants.REQUEST_METHOD_GET)
        response=connector.triggerRequest()
        return response.json()['Email']

class ZohoOAuthTokens(object):
    '''
    This class is to encapsulate the OAuth tokens
    '''
    def __init__(self, refresh_token,access_token,expiry_time,user_email=None):
        '''
        Constructor
        '''
        self.refreshToken=refresh_token
        self.accessToken=access_token
        self.expiryTime=expiry_time
        self.userEmail=user_email
        
    def getAccessToken(self):
        if((self.expiryTime-self.getCurrentTimeInMillis())>10):
            return self.accessToken
        else:
            return ZohoOAuthException("Access token got expired!")
    @staticmethod
    def getCurrentTimeInMillis():
        import time
        return int(round(time.time() * 1000))
    def setUserEmail(self,userEmail):
        self.userEmail=userEmail