'''
Created on Jul 31, 2017

@author: sumanth-3058
'''
from com.zoho.crm.library.common.Utility import HTTPConnector
from com.zoho.crm.library.setup.ZCRMRestClient import ZCRMRestClient
from com.zoho.oauth.client.OAuthClient import ZohoOAuth
from com.zoho.crm.library.crud.Operations import ZCRMModule
import threading
threadLocal=threading.local()
class MyThread(threading.Thread):
    def __init__(self,email):
        super(MyThread,self).__init__()
        self.local=threadLocal
        self.email=email
    def run(self):
        self.local.email=self.email
        print self.local.email
    
class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def test(self):
        thread=threading.Thread(name='sumanth.chilka+pyhtonautomation@zohocorp.com')
        thread.start()
        #thread.__setattr__('email','sumanth.chilka+pyhtonautomation@zohocorp.com')
        ##print threading.currentThread.getName()
        #threading.local().email='sumanth.chilka+pyhtonautomation@zohocorp.com'
        #threading.local().__dict__['email']='sumanth.chilka+pyhtonautomation@zohocorp.com'
        #threading.local().email='sumanth.chilka+pyhtonautomation@zohocorp.com'
        #threading.currentThread.__setattr__('email','sumanth.chilka+pyhtonautomation@zohocorp.com')
        #threadLocal.userEmail='sumanth.chilka+pyhtonautomation@zohocorp.com'
        t1=MyThread('sumanth')
        t1.start()
        print t1.email
        print threading.current_thread().name
        ZCRMRestClient.initialize()
        ZCRMModule.getInstance('Leads').getRecord(440872000000162010)
        '''cliIns=ZohoOAuth.getClientInstance()
        grantToken='1000.c1bb6a1daf67ca93569f43a8d475c25b.d496850a04b7b6d52abf1866639d1202'
        print cliIns.generateAccessToken(grantToken)
        
        url="https://crm.localzoho.com/crm/v2/Leads"
        headers={}
        headers['Authorization']="Zoho-authtoken 924003cd681fb99dc60cc8ad7e2e8f60"
        #headers['Content-type']='application/json'
        #headers['Accept']='text/plain'
        reqBody={"data":[{"Last_Name":"Python2"},{"Last_Name":"Python3"}]}
        connector=HTTPConnector.getInstance(url,{},headers,reqBody,"POST",'data',False)
        connector.triggerRequest()
        '''
        
obj=MyClass()
obj.test()