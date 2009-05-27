
from urllib2   import urlopen
from datetime  import datetime
import SOAPpy

class JiraAttachement(object):
    fields = ('filename', 'filesize', 'mimetype', 'author', 'created', 'id')
    default_base_url = 'http://issues.apache.org/jira/secure/attachment/'
    
    def __init__(self, attachment, base_url=default_base_url):
        for k in self.fields:
            setattr(self, k, attachment[k])
        self.base_url = base_url
        
        # Convert 'created' tuple to a proper datetime object
        if isinstance(self.created, tuple):
            self.created = datetime(*[int(i) for i in self.created])
            
    def get_download_url(self):
        return "%s/%s/%s" % (self.base_url.rstrip('/'), self.id, self.filename)
    
    def get_attached_file(self):
        return urlopen(self.get_download_url())

class JiraClient(object):
    default_base_url = 'https://issues.apache.org/jira'
    
    def __init__(self, user, passwd, url=default_base_url):
        self.user = user
        self.passwd = passwd
        self.url = url.rstrip("/")
        self.token, self.client = None, None
        self.__connect()
    
    def __connect(self):
        handle = urlopen(self.url + "/rpc/soap/jirasoapservice-v2?wsdl")
        self.client = SOAPpy.WSDL.Proxy(handle)
        self.token = self.client.login(self.user, self.passwd)
        
    def get_attachments(self, issue):
        resultset = []
        for a in self.client.getAttachmentsFromIssue(self.token, issue.upper()):
            resultset.append(JiraAttachement(a))
        return resultset

# vi:ai sw=4 ts=4 tw=0 et: