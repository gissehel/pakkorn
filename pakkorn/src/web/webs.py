#!/usr/bin/env python
# --------------------------------------------------------------

import socket
import urllib
import urllib2
import cookielib

# from resolvUrl.resolvUrl import ResolvUrl
# from SSLproxy import ConnectHTTPHandler
from SSLproxy import ConnectHTTPSHandler

# --------------------------------------------------------------

DEFAULT_AGENT = "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)"

# --------------------------------------------------------------

class AppURLopener(urllib.FancyURLopener):
    def __init__(self, version, *args):
        self.version = version
        urllib.FancyURLopener.__init__(self, *args)

# --------------------------------------------------------------

class WebUrllib(object) :
    def __init__( self, agent = DEFAULT_AGENT, http_proxy=None  ) :
        # http_proxy is not used now.

        self._agent = agent
        urllib._urlopener = AppURLopener(agent)

    def get ( self, url, file=None, encoding='utf-8' ) :
        result = ""
        url = url.encode(encoding)
        try :
            if file == None :
                f = urllib.urlopen( url )
                for line in f.readlines() :
                    result += line
            else :
                result = urllib.urlretrieve( url, file )
                result = result[0]
        except IOError :
            pass
        except socket.error :
            pass
        return result

    def post(self, *args, **kwargs) :
        raise Exception("Not Implemented")

    def cookies(self) :
        return None

# --------------------------------------------------------------

class WebUrllib2(object) :
    _default_result = None

    def __init__( self, agent = DEFAULT_AGENT, http_proxy=None ) :
        self._agent = agent

        openers = []

        if http_proxy is not None :
            # Look like urllib2 default proxy works better than ConnectHTTPHandler
            #openers.append(ConnectHTTPHandler(proxy="%s:%s" % (http_proxy[0],http_proxy[1]),debuglevel=1))
            openers.append(urllib2.ProxyHandler({"http" : "http://%s:%s" % (http_proxy[0],http_proxy[1])}))

            openers.append(ConnectHTTPSHandler(proxy="%s:%s" % (http_proxy[0],http_proxy[1])))


        self._cookiejar = cookielib.LWPCookieJar()
        openers.append(urllib2.HTTPCookieProcessor(self._cookiejar))

        opener = urllib2.build_opener(*openers)
        urllib2.install_opener(opener)

    def get ( self, url, postargs=None, file=None, encoding='utf-8', cookie=None ) :
        result = self._default_result

        url = url.encode(encoding)
        postdata = None

        if postargs != None :
            postdata = urllib.urlencode(postargs)

        header = {'User-agent' : self._agent}
        if cookie :
            header['Cookie']=cookie

        #print self._cookiejar
        #print url
        request = urllib2.Request(url, postdata, header)

        #print "[ %s ]" % self._cookiejar._cookies_for_request(request)
        self._cookiejar.add_cookie_header(request)


        try :
            f = urllib2.urlopen( request )
            if file != None :
                MAXSIZE = 8192
                tembuffer = f.read(MAXSIZE)
                handle = open(file,'wb')
                while tembuffer != '' :
                    handle.write(tembuffer)
                    tembuffer = f.read(MAXSIZE)
                handle.close()
                result = file
            else :
                result = f.read()
        except IOError :
            print "IOError"
            pass
        except socket.error :
            print "socket.error"
            pass
        return result

    def post ( self, *args, **kwargs ) :
        return self.get(*args,**kwargs)

    def cookies(self) :
        return self._cookiejar

# --------------------------------------------------------------

class WebDeprecated( WebUrllib2 ) :
    _default_result = ""

Web = WebUrllib2

# --------------------------------------------------------------

if __name__ == "__main__" :
    web = Web()
    print "%s\n-------------------" % web.get("http://giss.mine.nu/")

# --------------------------------------------------------------
