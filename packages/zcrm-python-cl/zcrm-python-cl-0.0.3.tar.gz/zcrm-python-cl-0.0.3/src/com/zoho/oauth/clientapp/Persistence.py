'''
Created on Aug 16, 2017

@author: sumanth-3058
'''
from com.zoho.oauth.common.Utility import Logger
#import MySQLdb
import mysql.connector
class ZohoOAuthPersistenceHandler(object):
    '''
    This class deals with persistance of oauth related tokens
    '''
    def saveOAuthTokens(self,oAuthTokens):
        try:
            self.deleteOAuthTokens(oAuthTokens.userEmail)
            connection=self.getDBConnection()
            cursor=connection.cursor()
            #sqlQuery="INSERT INTO oauthtokens(useridentifier,accesstoken,refreshtoken,expirytime) VALUES('"+oAuthTokens.userEmail+"','"+oAuthTokens.accessToken+"','"+oAuthTokens.refreshToken+"',"+oAuthTokens.expiryTime+")";
            sqlQuery="INSERT INTO oauthtokens(useridentifier,accesstoken,refreshtoken,expirytime) VALUES(%s,%s,%s,%s)";
            data=(oAuthTokens.userEmail,oAuthTokens.accessToken,oAuthTokens.refreshToken,oAuthTokens.expiryTime)
            cursor.execute(sqlQuery,data)
            connection.commit()
        except Exception as ex:
            import logging
            Logger.addLog("Exception occured while saving oauthtokens into DB ",logging.ERROR,ex)
        finally:
            cursor.close()
            connection.close()    
        
    def getOAuthTokens(self,userEmail):
        try:
            connection=self.getDBConnection()
            cursor=connection.cursor()
            sqlQuery="SELECT * FROM oauthtokens where useridentifier='"+userEmail+"'"
            cursor.execute(sqlQuery)
        except Exception as ex:
            import logging
            Logger.addLog("Exception occured while fetching oauthtokens from DB ",logging.ERROR,ex)
        finally:
            cursor.close()
            connection.close()
    def deleteOAuthTokens(self,userEmail):
        try:
            connection=self.getDBConnection()
            cursor=connection.cursor()
            #sqlQuery="DELETE FROM oauthtokens where useridentifier='"+userEmail+"'"
            sqlQuery="DELETE FROM oauthtokens where useridentifier=%s"
            cursor.execute(sqlQuery,(userEmail,))
            connection.commit()
        except Exception as ex:
            import logging
            Logger.addLog("Exception occured while deleting oauthtokens from DB ",logging.ERROR,ex)
        finally:
            cursor.close()
            connection.close()
            
    def getDBConnection(self):
        connection=mysql.connector.connect(user='root', password='',host='127.0.0.1',database='zohooauth')
        return connection
        #connection=MySQLdb.connect(host="localhost",user="root",passwd="",db="zohooauth")
        #return connection
