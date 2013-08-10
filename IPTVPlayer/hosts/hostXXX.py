# -*- coding: utf-8 -*-

###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.ihost import IHost, CDisplayListItem, RetHost, CUrlItem
import Plugins.Extensions.IPTVPlayer.libs.pCommon as pCommon
from Plugins.Extensions.IPTVPlayer.iptvtools import printDBG, CSelOneLink
import Plugins.Extensions.IPTVPlayer.libs.urlparser as urlparser

###################################################
# FOREIGN import
###################################################
import re, urllib, urllib2, base64, math    
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.config import config, ConfigSelection, ConfigYesNo, ConfigText, getConfigListEntry, ConfigPIN
###################################################

###################################################
# Config options for HOST
###################################################
def GetConfigList():
    optionList = []
    return optionList
###################################################

###################################################
# Title of HOST
###################################################
def gettytul():
    return 'XXX'

class IPTVHost(IHost):
    LOGO_NAME = 'XXXlogo.png'
    PATH_TO_LOGO = resolveFilename(SCOPE_PLUGINS, 'Extensions/IPTVPlayer/icons/' + LOGO_NAME )

    def __init__(self):
        printDBG( "init begin" )
        self.host = Host()
        self.prevIndex = []
        self.currList = []
        self.prevList = []
        printDBG( "init end" )
        
    def isProtectedByPinCode(self):
        return True
    
    def getLogoPath(self):  
        return RetHost(RetHost.OK, value = [self.PATH_TO_LOGO])

    def getInitList(self):
        printDBG( "getInitList begin" )
        self.prevIndex = []
        self.currList = self.host.getInitList()
        self.host.setCurrList(self.currList)
        self.prevList = []
        printDBG( "getInitList end" )
        return RetHost(RetHost.OK, value = self.currList)

    def getListForItem(self, Index = 0, refresh = 0, selItem = None):
        printDBG( "getListForItem begin" )
        self.prevIndex.append(Index)
        self.prevList.append(self.currList)
        self.currList = self.host.getListForItem(Index, refresh, selItem)
        #self.currList = [ self.prevList[-1][Index] ]
        printDBG( "getListForItem end" )
        return RetHost(RetHost.OK, value = self.currList)

    def getPrevList(self, refresh = 0):
        printDBG( "getPrevList begin" )
        if(len(self.prevList) > 0):
            self.prevIndex.pop()
            self.currList = self.prevList.pop()
            self.host.setCurrList(self.currList)
            printDBG( "getPrevList end OK" )
            return RetHost(RetHost.OK, value = self.currList)
        else:
            printDBG( "getPrevList end ERROR" )
            return RetHost(RetHost.ERROR, value = [])

    def getCurrentList(self, refresh = 0):
        printDBG( "getCurrentList begin" )
        #if refresh == 1
        #self.prevIndex[-1] #ostatni element prevIndex
        #self.prevList[-1]  #ostatni element prevList
        #tu pobranie listy dla dla elementu self.prevIndex[-1] z listy self.prevList[-1]  
        printDBG( "getCurrentList end" )
        return RetHost(RetHost.OK, value = self.currList)

    def getLinksForVideo(self, Index = 0, item = None):
        return RetHost(RetHost.NOT_IMPLEMENTED, value = [])
        
    def getResolvedURL(self, url):
        printDBG( "getResolvedURL begin" )
        if url != None and url != '':        
            ret = self.host.getResolvedURL(url)
            if ret != None and ret != '':        
               printDBG( "getResolvedURL ret: "+ret)
               list = []
               list.append(ret)
               printDBG( "getResolvedURL end OK" )
               return RetHost(RetHost.OK, value = list)
            else:
               printDBG( "getResolvedURL end" )
               return RetHost(RetHost.NOT_IMPLEMENTED, value = [])                
        else:
            printDBG( "getResolvedURL end" )
            return RetHost(RetHost.NOT_IMPLEMENTED, value = [])

    def getSearchResults(self, pattern, searchType = None):
        return RetHost(RetHost.NOT_IMPLEMENTED, value = [])

    ###################################################
    # Additional functions on class IPTVHost
    ###################################################

class Host:
    XXXversion = "8.0.0.0"
    XXXremote  = "0.0.0.0"
    currList = []
    MAIN_URL = ''
    
    def __init__(self):
        printDBG( 'Host __init__ begin' )
        self.cm = pCommon.common()
        self.currList = []

        _url = 'http://gitorious.org/iptv-host-xxx/iptv-host-xxx/blobs/master/IPTVPlayer/hosts/hostXXX.py'
        query_data = { 'url': _url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        try:
           data = self.cm.getURLRequestData(query_data)
           #printDBG( 'Host init data: '+data )
           r=re.search( r'XXXversion = &quot;(.+)&quot;',data)
           if r:
              printDBG( 'r' )
              self.XXXremote=r.groups(1)[0]
        except:
           printDBG( 'Host init query error' )
        printDBG( 'Host __init__ begin' )
        
    def setCurrList(self, list):
        printDBG( 'Host setCurrList begin' )
        self.currList = list
        printDBG( 'Host setCurrList begin' )
        return 

    def getInitList(self):
        printDBG( 'Host getInitList begin' )
        #self.currList = self.MAIN_MENU
        self.currList = self.listsItems(-1, '', 'main-menu')
        printDBG( 'Host getInitList end' )
        return self.currList

    def getListForItem(self, Index = 0, refresh = 0, selItem = None):
        printDBG( 'Host getListForItem begin' )
        valTab = []
        if len(self.currList[Index].urlItems) == 0:
           return valTab
        valTab = self.listsItems(Index, self.currList[Index].urlItems[0], self.currList[Index].urlSeparateRequest)
        self.currList = valTab
        printDBG( 'Host getListForItem end' )
        return self.currList

    def listsItems(self, Index, url, name = ''):
        printDBG( 'Host listsItems begin' )
        printDBG( 'Host listsItems url: '+url )
        valTab = []
        if name == 'main-menu':
           printDBG( 'Host listsItems begin name='+name )
           if self.XXXversion <> self.XXXremote and self.XXXremote <> "0.0.0.0":
              valTab.append(CDisplayListItem('---UPDATE---','UPDATE MENU',        CDisplayListItem.TYPE_CATEGORY, [''],                                     'UPDATE',  '', None)) 
           valTab.append(CDisplayListItem('TUBE8 mobile',   'm.tube8.com',        CDisplayListItem.TYPE_CATEGORY, ['http://m.tube8.com'],                   'tube8',   'http://cdn1.static.tube8.phncdn.com/images/t8logo.png', None)) 
           valTab.append(CDisplayListItem('YOUPORN mobile', 'mobile.youporn.com', CDisplayListItem.TYPE_CATEGORY, ['http://mobile.youporn.com'],            'youporn', 'http://cdn1.static.youporn.phncdn.com/cb/bundles/youpornwebfront/images/l_youporn_black.png', None)) 
           valTab.append(CDisplayListItem('PORNHUB mobile', 'm.pornhub.com',      CDisplayListItem.TYPE_CATEGORY, ['http://m.pornhub.com'],                 'pornhub', 'http://cdn1.static.pornhub.phncdn.com/images/pornhub_logo.png', None)) 
           valTab.append(CDisplayListItem('PORNHUB',        'www.pornhub.com',    CDisplayListItem.TYPE_CATEGORY, ['http://www.pornhub.com/categories'],    'fullpornhub', 'http://cdn1.static.pornhub.phncdn.com/images/pornhub_logo.png', None)) 
           valTab.append(CDisplayListItem('HDPORN',         'www.hdporn.net',     CDisplayListItem.TYPE_CATEGORY, ['http://www.hdporn.net/channels/'],      'hdporn',  'http://www.hdporn.net/gfx/logo.gif', None)) 
           valTab.append(CDisplayListItem('4TUBE',          'www.4tube.com',      CDisplayListItem.TYPE_CATEGORY, ['http://www.4tube.com/videos'],          '4tube',   'http://i.4tube.com/free-porn.png', None)) 
           valTab.append(CDisplayListItem('EPORNER',        'www.eporner.com',    CDisplayListItem.TYPE_CATEGORY, ['http://www.eporner.com/categories/'],   'eporner', 'http://static.eporner.com/new/logo.png', None)) 
           #valTab.append(CDisplayListItem('XHAMSTER',       'xhamster.com',       CDisplayListItem.TYPE_CATEGORY, ['http://xhamster.com/channels.php'],     'xhamster','http://eu-st.xhamster.com/images/tpl2/logo.png', None)) 
           valTab.append(CDisplayListItem('REDTUBE',        'www.redtube.com',    CDisplayListItem.TYPE_CATEGORY, ['http://www.redtube.com/channels'],      'redtube', 'http://img02.redtubefiles.com/_thumbs/design/logo/redtube_260x52_black.png', None)) 
           printDBG( 'Host listsItems end' )
           return valTab

        # ########## #
        if 'redtube' == name:
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://www.redtube.com' 
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url:'+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phCats = re.findall('class="video">.*?<a href="(.*?)" title="(.*?)">.*?src="(.*?)" />', data, re.S)
           if phCats:
              for (phUrl, phTitle, phImage) in phCats:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  valTab.append(CDisplayListItem(phTitle,phTitle,CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phUrl],'redtube-clips', phImage, None)) 
           valTab.insert(0,CDisplayListItem("Most Favored", "Most Favored", CDisplayListItem.TYPE_CATEGORY,["http://www.redtube.com/mostfavored?period=alltime"], 'redtube-clips', '',None))
           valTab.insert(0,CDisplayListItem("Most Viewed",  "Most Viewed",  CDisplayListItem.TYPE_CATEGORY,["http://www.redtube.com/mostviewed?period=alltime"],  'redtube-clips', '',None))
           valTab.insert(0,CDisplayListItem("Top Rated",    "Top Rated",    CDisplayListItem.TYPE_CATEGORY,["http://www.redtube.com/top?period=alltime"],         'redtube-clips', '',None))
           valTab.insert(0,CDisplayListItem("Newest",       "Newest",       CDisplayListItem.TYPE_CATEGORY,["http://www.redtube.com/"],                           'redtube-clips', '',None))
           printDBG( 'Host listsItems end' )
           return valTab
        if 'redtube-clips' == name:
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url: '+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phMovies = re.findall('class="video".*?<a href="(.*?)".*?title="(.*?)".*?class="te" src="(.*?)".*?class="time".*?span class="d">(.*?)</span>.*?style="float:left;">(.*?)</div>', data, re.S)
           if phMovies:
              for (phUrl, phTitle, phImage, phRuntime, phViews) in phMovies:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phRuntime: '+phRuntime )
                  printDBG( 'Host listsItems phViews: '+phViews )
                  valTab.append(CDisplayListItem(phTitle,'['+phRuntime+'] ['+phViews+'] '+phTitle,CDisplayListItem.TYPE_VIDEO, [CUrlItem('', self.MAIN_URL+phUrl, 1)], 0, phImage, None)) 
           match = re.findall('navNext.*?<b>Next', data, re.S)
           if match:
              printDBG( 'Host listsItems page match: '+match[0] )
              match = re.findall('href.*?"(.*?)"', match[0], re.S)
           if match:
              for phUrl in match:
                  printDBG( 'Host listsItems page phUrl: '+phUrl )
                  valTab.append(CDisplayListItem('Page', 'Page: '+phUrl, CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phUrl], name, '', None))                
           printDBG( 'Host listsItems end' )
           return valTab

        # ########## #
        if 'xhamster' == name:
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://xhamster.com' 
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url:'+url )
              return valTab
           printDBG( 'Host listsItems data: '+data )
           parse = re.search('title">Straight</div>(.*?)iconTrans"></div>', data, re.S)
           phCats = re.findall('<a\sclass="btnBig"\shref="(.*?)1.html">.*?\n\s\s+([a-z].*?)</a>', parse.group(1), re.S|re.I)
           if phCats:
              for (phUrl, phTitle) in phCats:
                  phTitle = phTitle.strip(' ')
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  valTab.append(CDisplayListItem(phTitle,phTitle,CDisplayListItem.TYPE_CATEGORY, [phUrl],'xhamster-clips', '', None)) 
           valTab.insert(0,CDisplayListItem("New",       "New",       CDisplayListItem.TYPE_CATEGORY,["http://xhamster.com/new/"], 'xhamster-clips', '',None))
           printDBG( 'Host listsItems end' )
           return valTab
        if 'xhamster-clips' == name:
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url: '+url )
              return valTab
           printDBG( 'Host listsItems data: '+data )
           if re.search('vDate', data, re.S):
              parse = re.search('<div\sclass=\'vDate(.*)</html>', data, re.S)
           else:
              parse = re.search('<html>(.*)</html>', data, re.S)
           phMovies = re.findall('class=\'video\'><a\shref=\'(.*?/movies/.*?)\'.*?class=\'hRotator\'\s><img\ssrc=\'(.*?)\'.*?alt="(.*?)".*?start2.*?<b>(.*?)</b>', parse.group(1), re.S)
           if phMovies:
              for (phUrl, phImage, phTitle, phRuntime) in phMovies:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phRuntime: '+phRuntime )
                  valTab.append(CDisplayListItem(phTitle,'['+phRuntime+'] '+phTitle,CDisplayListItem.TYPE_VIDEO, [CUrlItem('', phUrl, 1)], 0, phImage, None)) 
           match = re.findall('<center> <div class="numlist2">.*?</center>', data, re.S)
           if match:
              printDBG( 'Host listsItems page match: '+match[0] )
              match = re.findall("<a href='(.*?)'", match[0], re.S)
           if match:
              for phUrl in match:
                  printDBG( 'Host listsItems page phUrl: '+phUrl )
                  valTab.append(CDisplayListItem('Page', 'Page: '+phUrl, CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phUrl], name, '', catUrl))                
           printDBG( 'Host listsItems end' )
           return valTab

        # ########## #
        if 'eporner' == name:
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://www.eporner.com' 
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url:'+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phCats = re.findall('class="categoriesbox" id=".*?"><a href="(.*?)" title="(.*?)"><img src="(.*?)"', data, re.S)
           if phCats:
              for (phUrl, phTitle, phImage) in phCats:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  phTitle = phTitle.replace(' movies', '')
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  valTab.append(CDisplayListItem(phTitle,phTitle,CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phUrl],'eporner-clips', phImage, phUrl)) 
           valTab.insert(0,CDisplayListItem("HD",        "HD",        CDisplayListItem.TYPE_CATEGORY,["http://www.eporner.com/hd/"], 'eporner-clips', '','/hd/'))
           valTab.insert(0,CDisplayListItem("Top Rated", "Top Rated", CDisplayListItem.TYPE_CATEGORY,["http://www.eporner.com/top_rated/"], 'eporner-clips', '','/top_rated/'))
           valTab.insert(0,CDisplayListItem("Popular",   "Popular",   CDisplayListItem.TYPE_CATEGORY,["http://www.eporner.com/weekly_top/"], 'eporner-clips', '','/weekly_top/'))
           valTab.insert(0,CDisplayListItem("On Air",    "On Air",    CDisplayListItem.TYPE_CATEGORY,["http://www.eporner.com/currently/"], 'eporner-clips', '','/currently/'))
           valTab.insert(0,CDisplayListItem("New",       "New",       CDisplayListItem.TYPE_CATEGORY,["http://www.eporner.com/"], 'eporner-clips', '',''))
           printDBG( 'Host listsItems end' )
           return valTab
        if 'eporner-clips' == name:
           printDBG( 'Host listsItems begin name='+name )
           catUrl = self.currList[Index].possibleTypesOfSearch
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url: '+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           if url == "http://www.eporner.com/top_rated/":
              phMovies = re.findall('<div\sclass="mbtit"><a\shref="(.*?)"\stitle="(.*?)".*?src="(.*?)".*?<span>.*?<\/span>\s(.*?)<\/div>', data, re.S)
              if phMovies:
                 for (phUrl, phTitle, phImage, phRuntime) in phMovies:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phRuntime: '+phRuntime )
                  valTab.append(CDisplayListItem(phTitle,'['+phRuntime+'] '+phTitle,CDisplayListItem.TYPE_VIDEO, [CUrlItem('', self.MAIN_URL+phUrl, 1)], 0, phImage, None)) 
           else:
              phMovies = re.findall('<div\sclass="mbtit"><a\shref="(.*?)"\stitle="(.*?)".*?src="(.*?)".*?<span>.*?<\/span>\s(.*?)<\/div>.*?eye.png.*?<\/span>\s(.*?)<\/div>', data, re.S)
              if phMovies:
                 for (phUrl, phTitle, phImage, phRuntime, phViews) in phMovies:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phRuntime: '+phRuntime )
                  printDBG( 'Host listsItems phViews: '+phViews )
                  valTab.append(CDisplayListItem(phTitle,'['+phRuntime+'] [ Views: '+phViews+'] '+phTitle,CDisplayListItem.TYPE_VIDEO, [CUrlItem('', self.MAIN_URL+phUrl, 1)], 0, phImage, None)) 
           match = re.findall('<center> <div class="numlist2">.*?</center>', data, re.S)
           if match:
              printDBG( 'Host listsItems page match: '+match[0] )
              match = re.findall("<a href='(.*?)'", match[0], re.S)
           if match:
              for phUrl in match:
                  printDBG( 'Host listsItems page phUrl: '+phUrl )
                  valTab.append(CDisplayListItem('Page', 'Page: '+phUrl, CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phUrl], name, '', catUrl))                
           printDBG( 'Host listsItems end' )
           return valTab

        # ########## #
        if 'fullpornhub' == name:
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://www.pornhub.com' 
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url:'+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phCats = re.findall('<div\sclass="category-wrapper">.*?<a\shref="(/video\?c=.*?)"><img\ssrc="(.*?)".*?alt="(.*?)"', data, re.S)
           if phCats:
              for (phUrl, phImage, phTitle) in phCats:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  valTab.append(CDisplayListItem(phTitle,phTitle,CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phUrl],'fullpornhub-clips', phImage, None)) 
                  valTab.sort()
           valTab.insert(0,CDisplayListItem("HD",         "HD",          CDisplayListItem.TYPE_CATEGORY,["http://www.pornhub.com/video?c=38"], 'fullpornhub-clips', 'http://cdn1a.static.pornhub.phncdn.com/images/categories/38.jpg',None))
           valTab.insert(0,CDisplayListItem("Longest",    "Longest",     CDisplayListItem.TYPE_CATEGORY,["http://www.pornhub.com/video?o=lg"], 'fullpornhub-clips', '',None))
           valTab.insert(0,CDisplayListItem("Top Rated",  "Top Rated",   CDisplayListItem.TYPE_CATEGORY,["http://www.pornhub.com/video?o=tr"], 'fullpornhub-clips', '',None))
           valTab.insert(0,CDisplayListItem("Most Viewed","Most Viewed", CDisplayListItem.TYPE_CATEGORY,["http://www.pornhub.com/video?o=mv"], 'fullpornhub-clips', '',None))
           valTab.insert(0,CDisplayListItem("Most Recent","Most Recent", CDisplayListItem.TYPE_CATEGORY,["http://www.pornhub.com/video?o=mr"], 'fullpornhub-clips', '',None))
           printDBG( 'Host listsItems end' )
           return valTab
        if 'fullpornhub-clips' == name:
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url: '+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phMovies = re.findall('<div\sclass="wrap">.*?<a\shref="(.*?)".*?\stitle="(.*?)".*?data-mediumthumb="(.*?)".*?<var\sclass="duration">(.*?)</var>.*?<span\sclass="views"><var>(.*?)<.*?<var\sclass="added">(.*?)<', data, re.S)
           if phMovies:
              for (phUrl, phTitle, phImage, phRuntime, phViews, phAdded) in phMovies:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phRuntime: '+phRuntime )
                  printDBG( 'Host listsItems phViews: '+phViews )
                  printDBG( 'Host listsItems phAdded: '+phAdded )
                  valTab.append(CDisplayListItem(phTitle,'['+phRuntime+'] [ Views: '+phViews+'] [Added: '+phAdded+'] '+phTitle,CDisplayListItem.TYPE_VIDEO, [CUrlItem('', phUrl, 1)], 0, phImage, None)) 
           match = re.findall('<li class="page_next"><a href="(.*?)"', data, re.S)
           if match:
              valTab.append(CDisplayListItem('Next', 'Next Page', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+match[0].replace('&amp;','&')], name, '', None))        
           printDBG( 'Host listsItems end' )
           return valTab
        
        # ########## #
        if '4tube' == name:
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://www.4tube.com' 
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url:'+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           parse = re.search('Popular Tags(.*?)End Section', data, re.S)
           phCats = re.findall('<a class=".*?" href="(.*?)">(.*?)</a>', parse.group(1), re.S)
           if phCats:
              for (phUrl, phTitle) in phCats:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  phTitle = phTitle.title()
                  valTab.append(CDisplayListItem(phTitle,phTitle,CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phUrl],'4tube-clips', '', None)) 
           #valTab.sort()
           valTab.insert(0,CDisplayListItem("Websites","Websites",   CDisplayListItem.TYPE_CATEGORY,["http://www.4tube.com/sites"]  ,            '4tube-sites',    '',None))
           valTab.insert(0,CDisplayListItem("Pornstars","Pornstars", CDisplayListItem.TYPE_CATEGORY,["http://www.4tube.com/pornstars"],          '4tube-pornstars','',None))
           valTab.insert(0,CDisplayListItem("Full","Full",           CDisplayListItem.TYPE_CATEGORY,["http://www.4tube.com/videos/full-length"], '4tube-clips',    '',None))
           valTab.insert(0,CDisplayListItem("Featured","Featured",   CDisplayListItem.TYPE_CATEGORY,["http://www.4tube.com/featured"],           '4tube-clips',    '',None))
           valTab.insert(0,CDisplayListItem("Lastest","Lastest",     CDisplayListItem.TYPE_CATEGORY,["http://www.4tube.com/videos"],             '4tube-clips',    '',None))
           printDBG( 'Host listsItems end' )
           return valTab
        if '4tube-sites' == name:
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url: '+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phMovies = re.findall('class="siteInfo"><span class="name"><a href="(.*?)">(.*?)</a></span><a href=".*?"><img class="thumb" src="(.*?)"',data,re.S) 
           if phMovies:
              for (phUrl, phTitle, phImage) in phMovies:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  valTab.append(CDisplayListItem(phTitle,phTitle,CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phUrl], '4tube-clips', phImage, None)) 
           match = re.findall('<a class="page " href="(.*?)"', data, re.S)
           if match:
              for (phPageUrl) in match: 
                  printDBG( 'Host listsItems phPageUrl: '  +phPageUrl )
                  valTab.append(CDisplayListItem('Page', phPageUrl, CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phPageUrl], '4tube-sites', '', None))                
           match = re.findall('<a class="last" href="(.*?)" title="Last page">', data, re.S)
           if match:
              for (phPageUrl) in match: 
                  printDBG( 'Host listsItems phPageUrl: '  +phPageUrl )
                  valTab.append(CDisplayListItem('Last Page', phPageUrl, CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phPageUrl], name, '', None))                
           match = re.findall('<link rel="next" href="(.*?)"', data, re.S)
           if match:
              valTab.append(CDisplayListItem('Next', 'Next Page', CDisplayListItem.TYPE_CATEGORY, [match[0]], '4tube-sites', '', None))                
           printDBG( 'Host listsItems end' )
           return valTab
        if '4tube-pornstars' == name:
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url: '+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phMovies = re.findall('pornstarInfoLarge_pornstar"><a title=.*?href="(.*?)".*?class="thumb" src="(.*?)" title="(.*?)"',data,re.S) 
           if phMovies:
              for (phUrl, phImage, phTitle) in phMovies:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  valTab.append(CDisplayListItem(phTitle,phTitle,CDisplayListItem.TYPE_CATEGORY, [phUrl], '4tube-clips', phImage, None)) 
           match = re.findall('<a class="page " href="(.*?)"', data, re.S)
           if match:
              for (phPageUrl) in match: 
                  printDBG( 'Host listsItems phPageUrl: '  +phPageUrl )
                  valTab.append(CDisplayListItem('Page', phPageUrl, CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phPageUrl], name, '', None))                
           match = re.findall('<a class="last" href="(.*?)" title="Last page">', data, re.S)
           if match:
              for (phPageUrl) in match: 
                  printDBG( 'Host listsItems phPageUrl: '  +phPageUrl )
                  valTab.append(CDisplayListItem('Last Page', phPageUrl, CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phPageUrl], name, '', None))                
           match = re.findall('<link rel="next" href="(.*?)"', data, re.S)
           if match:
              valTab.append(CDisplayListItem('Next', 'Next Page', CDisplayListItem.TYPE_CATEGORY, [match[0]], name, '', None))                
           printDBG( 'Host listsItems end' )
           return valTab
        if '4tube-clips' == name:
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url: '+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phMovies = re.findall('class="videoInfo-item".*?href="(.*?)".*?class="thumb" src="(.*?)" title="(.*?)".*?<span class="length">(.*?)</span>',data,re.S) 
           if phMovies:
              for (phUrl, phImage, phTitle, phRuntime) in phMovies:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phRuntime: '+phRuntime )
                  valTab.append(CDisplayListItem(phTitle,phRuntime+' '+phTitle,CDisplayListItem.TYPE_VIDEO, [CUrlItem('', phUrl, 1)], 0, phImage, None)) 
           match = re.findall('<a class="page " href="(.*?)"', data, re.S)
           if match:
              for (phPageUrl) in match: 
                  printDBG( 'Host listsItems phPageUrl: '  +phPageUrl )
                  valTab.append(CDisplayListItem('Page', phPageUrl, CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phPageUrl], name, '', None))                
           match = re.findall('<a class="last" href="(.*?)" title="Last page">', data, re.S)
           if match:
              for (phPageUrl) in match: 
                  printDBG( 'Host listsItems phPageUrl: '  +phPageUrl )
                  valTab.append(CDisplayListItem('Last Page', phPageUrl, CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phPageUrl], name, '', None))                
           match = re.findall('<link rel="next" href="(.*?)"', data, re.S)
           if match:
              valTab.append(CDisplayListItem('Next', 'Next Page', CDisplayListItem.TYPE_CATEGORY, [match[0]], name, '', None))                
           printDBG( 'Host listsItems end' )
           return valTab

        # ########## #
        if 'hdporn' == name:
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://www.hdporn.net'
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url:'+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phCats = re.findall('class="content">.*?href="(.*?)".*?src="(.*?)".*?alt="(.*?)"', data, re.S)
           if phCats:
              for (phUrl, phImage, phTitle) in phCats:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  valTab.append(CDisplayListItem(phTitle,phTitle,CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+phUrl],'hdporn-clips', phImage, phUrl)) 
           #valTab.sort()
           valTab.insert(0,CDisplayListItem("Top Rated","Top Rated",           CDisplayListItem.TYPE_CATEGORY,[self.MAIN_URL+"/top-rated/"]  , 'hdporn-clips','',''))
           valTab.insert(0,CDisplayListItem("Most Popular","Most Popular",     CDisplayListItem.TYPE_CATEGORY,[self.MAIN_URL+"/most-viewed/"], 'hdporn-clips','',''))
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'hdporn-clips':
           printDBG( 'Host listsItems begin name='+name )
           catUrl = self.currList[Index].possibleTypesOfSearch
           printDBG( 'Host listsItems cat-url: '+catUrl )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              printDBG( 'Host listsItems query error url: '+url )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           phMovies = re.findall('class="content">.*?<a href="(.*?)" title="(.*?)".*?<img src="(.*?)".*?TIME:  (.*?)</div>', data, re.S)
           if phMovies:
              for (phUrl, phTitle, phImage, phRuntime) in phMovies:
                  printDBG( 'Host listsItems phUrl: '  +phUrl )
                  printDBG( 'Host listsItems phTitle: '+phTitle )
                  printDBG( 'Host listsItems phImage: '+phImage )
                  printDBG( 'Host listsItems phRuntime: '+phRuntime )
                  valTab.append(CDisplayListItem(phTitle,'['+phRuntime+'] '+phTitle,CDisplayListItem.TYPE_VIDEO, [CUrlItem('', phUrl, 1)], 0, phImage, None)) 
           match = re.findall('<div id="pagination">.*?</div>', data, re.S)
           printDBG( 'Host listsItems len match: '+str(len(match)))
           #printDBG( 'Host listsItems match: '+match[0])
           match = re.findall("</a><a href='(.*?)'>", match[0], re.S)
           printDBG( 'Host listsItems len match: '+str(len(match)))
           #printDBG( 'Host listsItems match: '+match[0])
           if len(match)>0:
              valTab.append(CDisplayListItem('Next', 'Next Page', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+catUrl+match[0]], 'hdporn-clips', '', catUrl))                
           printDBG( 'Host listsItems end' )
           return valTab

        # ########## #
        if 'tube8' == name:
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://m.tube8.com' 
           valTab.append(CDisplayListItem('LAST',       'Last',       CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL],                    'tube8-last', '', None)) 
           valTab.append(CDisplayListItem('CATEGORIES', 'Categories', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+'/category/browse'], 'tube8-categories', '', None)) 
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'tube8-last':
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           match = re.compile('<div class="scene_box">.+?background: url(.+?) no-repeat.+?style="margin: 0;".+?<a href="(.+?)" class="bold".+?				(.+?)<span style=.+?<p>(.+?)</p>.+?<div style="float: right;" class="bold"><span>(.+?)</span>.+?<div class="clear"></div>', re.DOTALL).findall(data)
           if len(match) == 0:
              match = re.compile('<div class="scene_box">.+?background: url(.+?) no-repeat.+?style="margin: 0;".+?<a href="(.+?)" class="bold".+?				(.+?)</a>.+?<p>(.+?)</p>.+?<div style="float: right;" class="bold"><span>(.+?)</span>.+?<div class="clear"></div>', re.DOTALL).findall(data)
           printDBG( 'Host listsItems len match: '+str(len(match)))
           for i in range(len(match)):
              for j in range(len(match[i])):
                printDBG( 'Host listsItems match: '+str(i)+','+str(j)+': '+match[i][j])
              valTab.append(CDisplayListItem(match[i][2], '['+match[i][4]+'] ['+match[i][3]+'] '+match[i][2], CDisplayListItem.TYPE_VIDEO, [CUrlItem('', self.MAIN_URL+match[i][1], 1)], 0, match[i][0][1:-1], None)) 
           match = re.compile('<div class="next_nav">.+?<a href="(.+?)">NEXT</a>', re.DOTALL).findall(data)
           if len(match)>0:
              valTab.append(CDisplayListItem('Next', 'Next Page', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+match[0]], 'tube8-last', '', None))                
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'tube8-categories':
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           match = re.compile('<h2><a href="(.+?)">(.+?)</a></h2>', re.DOTALL).findall(data)
           printDBG( 'Host listsItems len match: '+str(len(match)))
           for i in range(len(match)):
              for j in range(len(match[i])):
                printDBG( 'Host listsItems match: '+str(i)+','+str(j)+': '+match[i][j])
              valTab.append(CDisplayListItem(match[i][1], match[i][1], CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+match[i][0]], 'tube8-last', '', None)) 
           printDBG( 'Host listsItems end' )
           return valTab

        # ########## #
        if 'youporn' == name:
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://mobile.youporn.com' 
           valTab.append(CDisplayListItem('LAST',       'Last',       CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL],                    'youporn-last', '', None)) 
           valTab.append(CDisplayListItem('CATEGORIES', 'Categories', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+'/category/browse'], 'youporn-categories', '', None)) 
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'youporn-last':
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           match = re.compile(   '<div class="video_box".+?background: url(.+?) no-repeat.+?<h2 class="h5"><a href="(.+?)">\n(.+?)          .+?<span>Length:.+?			(.+?)		</p>', re.DOTALL).findall(data)
           printDBG( 'Host listsItems len match: '+str(len(match)))
           for i in range(len(match)):
              for j in range(len(match[i])):
                printDBG( 'Host listsItems match: '+str(i)+','+str(j)+': '+match[i][j])
              valTab.append(CDisplayListItem(match[i][2].replace('<br />',' '), '['+match[i][3]+'] '+match[i][2].replace('<br />',' '), CDisplayListItem.TYPE_VIDEO, [CUrlItem('', self.MAIN_URL+match[i][1], 1)], 0, match[i][0][1:-1], None)) 
           match = re.compile('<div class="next_nav">.+?<a href="(.+?)">NEXT</a>', re.DOTALL).findall(data)
           if len(match)>0:
              valTab.append(CDisplayListItem('Next', 'Next Page', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+match[0]], 'youporn-last', '', None))                
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'youporn-categories':
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           match = re.compile('<h2><a href="(.+?)">(.+?)</a></h2>', re.DOTALL).findall(data)
           printDBG( 'Host listsItems len match: '+str(len(match)))
           for i in range(len(match)):
              for j in range(len(match[i])):
                printDBG( 'Host listsItems match: '+str(i)+','+str(j)+': '+match[i][j])
              valTab.append(CDisplayListItem(match[i][1], match[i][1], CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+match[i][0]], 'youporn-last', '', None)) 
           printDBG( 'Host listsItems end' )
           return valTab

        # ########## #
        if 'pornhub' == name:
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://m.pornhub.com' 
           valTab.append(CDisplayListItem('LAST',       'Last',       CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL],                    'pornhub-last', '', None)) 
           valTab.append(CDisplayListItem('CATEGORIES', 'Categories', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+'/category/browse'], 'pornhub-categories', '', None)) 
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'pornhub-last':
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           match = re.compile('<div class="video_box".+?background: url(.+?) no-repeat.+?<h2 class="h5"><a href="(.+?)" >(.+?)</a></h2>.+?<span>Length:.+?			(.+?)		</p>', re.DOTALL).findall(data)
           printDBG( 'Host listsItems len match: '+str(len(match)))
           for i in range(len(match)):
              for j in range(len(match[i])):
                printDBG( 'Host listsItems match: '+str(i)+','+str(j)+': '+match[i][j])
              valTab.append(CDisplayListItem(match[i][2].replace('<br />',' '), '['+match[i][3]+'] '+match[i][2].replace('<br />',' '), CDisplayListItem.TYPE_VIDEO, [CUrlItem('', self.MAIN_URL+match[i][1], 1)], 0, match[i][0][1:-1], None)) 
           match = re.compile('<div class="next_nav">.+?<a href="(.+?)">NEXT</a>', re.DOTALL).findall(data)
           if len(match)>0:
              valTab.append(CDisplayListItem('Next', 'Next Page', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+match[0]], 'pornhub-last', '', None))                
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'pornhub-categories':
           printDBG( 'Host listsItems begin name='+name )
           query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              data = self.cm.getURLRequestData(query_data)
           except:
              printDBG( 'Host listsItems query error' )
              return valTab
           #printDBG( 'Host listsItems data: '+data )
           match = re.compile('<h2><a href="(.+?)">(.+?)</a></h2>', re.DOTALL).findall(data)
           printDBG( 'Host listsItems len match: '+str(len(match)))
           for i in range(len(match)):
              for j in range(len(match[i])):
                printDBG( 'Host listsItems match: '+str(i)+','+str(j)+': '+match[i][j])
              valTab.append(CDisplayListItem(match[i][1], match[i][1], CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+match[i][0]], 'pornhub-last', '', None)) 
           printDBG( 'Host listsItems end' )
           return valTab
        # ########## #
        if 'UPDATE' == name:
           printDBG( 'Host listsItems begin name='+name )
           valTab.append(CDisplayListItem(self.XXXversion+' - Local version',   'Local  XXXversion', CDisplayListItem.TYPE_CATEGORY, [''], '', '', None)) 
           valTab.append(CDisplayListItem(self.XXXremote+ ' - Remote version',  'Remote XXXversion', CDisplayListItem.TYPE_CATEGORY, [''], '', '', None)) 
           valTab.append(CDisplayListItem('Update Now',   'Update Now', CDisplayListItem.TYPE_CATEGORY, [''], 'UPDATE-NOW', '', None)) 
           printDBG( 'Host listsItems end' )
           return valTab
        if 'UPDATE-NOW' == name:
           printDBG( 'Host listsItems begin name='+name )
           import os
           output = open('/tmp/iptv-host-xxx.tar.gz','wb')
           _url = 'http://gitorious.org/iptv-host-xxx/iptv-host-xxx/archive-tarball/master'
           query_data = { 'url': _url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
           try:
              output.write(self.cm.getURLRequestData(query_data))
              output.close()
              os.system('sync')
           except:
              if os.path.exists('/tmp/iptv-host-xxx.tar.gz'):
                 os.remove('/tmp/iptv-host-xxx.tar.gz')
              printDBG( 'Błąd pobierania master.tar.gz' )
              return []
           
           try: 
              os.system('cd /tmp; tar -xzf iptv-host-xxx.tar.gz; sync')
           except:
              printDBG( 'Błąd rozpakowania iptv-host-xxx.tar.gz' )
              os.system('rm -f /tmp/iptv-host-xxx.tar.gz')
              os.system('rm -rf /tmp/iptv-host-xxx-iptv-host-xxx')
              return []
           if not os.path.exists('/tmp/iptv-host-xxx-iptv-host-xxx/IPTVPlayer'):
              printDBG( 'Niepoprawny format pliku /tmp/iptv-host-xxx.tar.gz' )
              os.system('rm -f /tmp/iptv-host-xxx.tar.gz')
              os.system('rm -rf /tmp/iptv-host-xxx-iptv-host-xxx')
              return []
            
           try:
              os.system('cp -rf /tmp/iptv-host-xxx-iptv-host-xxx/IPTVPlayer/* /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/')
              os.system('sync')
           except:
              printDBG( 'blad kopiowania' )
              os.system('rm -f /tmp/iptv-host-xxx.tar.gz')
              os.system('rm -rf /tmp/iptv-host-xxx-iptv-host-xxx')
              return []
               
           valTab.append(CDisplayListItem('Update End. Please manual restart enigma2',   'Restart', CDisplayListItem.TYPE_CATEGORY, [''], '', '', None)) 
           os.system('rm -f /tmp/iptv-host-xxx.tar.gz')
           os.system('rm -rf /tmp/iptv-host-xxx-iptv-host-xxx')
           printDBG( 'Host listsItems end' )
           return valTab

        return valTab

    def getResolvedURL(self, url):
        printDBG( 'Host getResolvedURL begin' )
        printDBG( 'Host getResolvedURL url: '+url )
        videoUrl = ''
        valTab = []
        query_data = {'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True}
        try:
           data = self.cm.getURLRequestData(query_data)
           #printDBG( 'Host getResolvedURL data: '+data )
        except:
           printDBG( 'Host getResolvedURL query error' )
           return videoUrl

        if self.MAIN_URL == 'http://www.redtube.com':
           videoPage = re.findall("source src='(.*?)'", data, re.S)
           if videoPage:
              for (phurl) in videoPage:
                url = '%s' % (phurl)
                videos = urllib.unquote(url)
                return videos
           return ''

        if self.MAIN_URL == 'http://xhamster.com':
           xhServer = re.findall("'srv': '(.*?)'", data)
           xhFile = re.findall("'file': '(.*?)'", data)
           if re.match('.*?http%3A', xhFile[0]):
              xhStream = urllib2.unquote(xhFile[0])
           else:
              xhStream = xhServer[0]+"/key="+xhFile[0]
           return xhStream
        
        if self.MAIN_URL == 'http://www.eporner.com':
           videoPage = re.findall(r"player4\\([^\\]*)\\", data, re.S)
           if videoPage:
              for phurl in videoPage:
                  printDBG( 'Host getResolvedURL phurl: '+phurl )
                  xml = 'http://www.eporner.com/config5%s' % (phurl)
           printDBG( 'Host getResolvedURL xml: '+xml )
           try:
              data = self.cm.getURLRequestData({'url': xml, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True})
           except:
              printDBG( 'Host getResolvedURL query error xml' )
              return videoUrl
           videoPage = re.findall('<hd.file>(.*?)</hd.file>', data, re.S)
           if videoPage:
              for phurl in videoPage:
                  return phurl
           else:
              videoPage = re.findall('<file>(.*?)</file>', data, re.S)
              if videoPage:
                 for phurl in videoPage:
                     return phurl
           return ''

        if self.MAIN_URL == 'http://www.pornhub.com':
           match = re.compile('"video_url":"([^"]+)"').findall(data)
           if not match:
              match = re.compile('"quality_720p":"([^"]+)"').findall(data)
           if not match:
              match = re.compile('"quality_480p":"([^"]+)"').findall(data)
           if not match:
              match = re.compile('"quality_240p":"([^"]+)"').findall(data)
           fetchurl = match
           fetchurl = urllib2.unquote(match[0])
           match = re.compile('"video_title":"([^"]+)"').findall(data)
           title = urllib.unquote_plus(match[0])
           printDBG( 'Host getResolvedURL decrypt begin ' )
           printDBG( 'Host getResolvedURL fetchurl: '+fetchurl )
           printDBG( 'Host getResolvedURL title: '+title )
           phStream = decrypt(fetchurl, title, 256)
           if phStream:
              return phStream
           else: return ''

        if self.MAIN_URL == 'http://www.4tube.com':
           videoPage = re.findall('sources:\s\[\{"file":"(.*?)"', data, re.S)
           if videoPage:
              videoUrl = videoPage[0].replace('\/','/')
              return videoUrl
           else: return ''
        
        if self.MAIN_URL == 'http://www.hdporn.net':
           match = re.findall('<param name="flashvars" value="file=(.*?)&provider=', data, re.S)
           return match[0]
        if self.MAIN_URL == 'http://m.tube8.com':
           match = re.compile('<div class="play_video.+?<a href="(.+?)"', re.DOTALL).findall(data)
           return match[0]
        if self.MAIN_URL == 'http://mobile.youporn.com':
           match = re.compile('<div class="play_video.+?<a href="(.+?)"', re.DOTALL).findall(data)
           return match[0]
        if self.MAIN_URL == 'http://m.pornhub.com':
           match = re.compile('<div class="play_video.+?<a href="(.+?)"', re.DOTALL).findall(data)
           return match[0]

        #for phurl in match: printDBG( 'Host getResolvedURL phurl: '+phurl )
        #if len(match)>0:
        #   videoUrl = match[0]
        printDBG( 'Host getResolvedURL end' )
        return videoUrl




############################################
# functions for fullpornhub
############################################
def decrypt(ciphertext, password, nBits):
    printDBG( 'decrypt begin ' )
    blockSize = 16
    if not nBits in (128, 192, 256): return ""
    ciphertext = base64.b64decode(ciphertext)
#    password = password.encode("utf-8")

    nBytes = nBits//8
    pwBytes = [0] * nBytes
    for i in range(nBytes): pwBytes[i] = 0 if i>=len(password) else ord(password[i])
    key = Cipher(pwBytes, KeyExpansion(pwBytes))
    key += key[:nBytes-16]

    counterBlock = [0] * blockSize
    ctrTxt = ciphertext[:8]
    for i in range(8): counterBlock[i] = ord(ctrTxt[i])

    keySchedule = KeyExpansion(key)

    nBlocks = int( math.ceil( float(len(ciphertext)-8) / float(blockSize) ) )
    ct = [0] * nBlocks
    for b in range(nBlocks):
        ct[b] = ciphertext[8+b*blockSize : 8+b*blockSize+blockSize]
    ciphertext = ct

    plaintxt = [0] * len(ciphertext)

    for b in range(nBlocks):
        for c in range(4): counterBlock[15-c] = urs(b, c*8) & 0xff
        for c in range(4): counterBlock[15-c-4] = urs( int( float(b+1)/0x100000000-1 ), c*8) & 0xff

        cipherCntr = Cipher(counterBlock, keySchedule)

        plaintxtByte = [0] * len(ciphertext[b])
        for i in range(len(ciphertext[b])):
            plaintxtByte[i] = cipherCntr[i] ^ ord(ciphertext[b][i])
            plaintxtByte[i] = chr(plaintxtByte[i])
        plaintxt[b] = "".join(plaintxtByte)

    plaintext = "".join(plaintxt)
 #   plaintext = plaintext.decode("utf-8")
    return plaintext

Sbox = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

Rcon = [
    [0x00, 0x00, 0x00, 0x00],
    [0x01, 0x00, 0x00, 0x00],
    [0x02, 0x00, 0x00, 0x00],
    [0x04, 0x00, 0x00, 0x00],
    [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00],
    [0x20, 0x00, 0x00, 0x00],
    [0x40, 0x00, 0x00, 0x00],
    [0x80, 0x00, 0x00, 0x00],
    [0x1b, 0x00, 0x00, 0x00],
    [0x36, 0x00, 0x00, 0x00]
]

def Cipher(input, w):
    printDBG( 'cipher begin ' )
    Nb = 4
    Nr = len(w)/Nb - 1

    state = [ [0] * Nb, [0] * Nb, [0] * Nb, [0] * Nb ]
    for i in range(0, 4*Nb): state[i%4][i//4] = input[i]

    state = AddRoundKey(state, w, 0, Nb)

    for round in range(1, Nr):
        state = SubBytes(state, Nb)
        state = ShiftRows(state, Nb)
        state = MixColumns(state, Nb)
        state = AddRoundKey(state, w, round, Nb)

    state = SubBytes(state, Nb)
    state = ShiftRows(state, Nb)
    state = AddRoundKey(state, w, Nr, Nb)

    output = [0] * 4*Nb
    for i in range(4*Nb): output[i] = state[i%4][i//4]
    return output

def SubBytes(s, Nb):
    printDBG( 'subbytes begin ' )
    for r in range(4):
        for c in range(Nb):
            s[r][c] = Sbox[s[r][c]]
    return s

def ShiftRows(s, Nb):
    printDBG( 'shiftrows begin ' )
    t = [0] * 4
    for r in range (1,4):
        for c in range(4): t[c] = s[r][(c+r)%Nb]
        for c in range(4): s[r][c] = t[c]
    return s

def MixColumns(s, Nb):
    printDBG( 'mixcolumns begin ' )
    for c in range(4):
        a = [0] * 4
        b = [0] * 4
        for i in range(4):
            a[i] = s[i][c]
            b[i] = s[i][c]<<1 ^ 0x011b if s[i][c]&0x80 else s[i][c]<<1
        s[0][c] = b[0] ^ a[1] ^ b[1] ^ a[2] ^ a[3]
        s[1][c] = a[0] ^ b[1] ^ a[2] ^ b[2] ^ a[3]
        s[2][c] = a[0] ^ a[1] ^ b[2] ^ a[3] ^ b[3]
        s[3][c] = a[0] ^ b[0] ^ a[1] ^ a[2] ^ b[3]
    return s

def AddRoundKey(state, w, rnd, Nb):
    printDBG( 'addroundkey begin ' )
    for r in range(4):
        for c in range(Nb):
            state[r][c] ^= w[rnd*4+c][r]
    return state

def KeyExpansion(key):
    printDBG( 'keyexpansion begin ' )
    Nb = 4
    Nk = len(key)/4
    Nr = Nk + 6

    w = [0] * Nb*(Nr+1)
    temp = [0] * 4

    for i in range(Nk):
        r = [key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]]
        w[i] = r

    for i in range(Nk, Nb*(Nr+1)):
        w[i] = [0] * 4
        for t in range(4): temp[t] = w[i-1][t]
        if i%Nk == 0:
            temp = SubWord(RotWord(temp))
            for t in range(4): temp[t] ^= Rcon[i/Nk][t]
        elif Nk>6 and i%Nk == 4:
            temp = SubWord(temp)
        for t in range(4): w[i][t] = w[i-Nk][t] ^ temp[t]
    return w

def SubWord(w):
    printDBG( 'subword begin ' )
    for i in range(4): w[i] = Sbox[w[i]]
    return w

def RotWord(w):
    printDBG( 'rotword begin ' )
    tmp = w[0]
    for i in range(3): w[i] = w[i+1]
    w[3] = tmp
    return w

def encrypt(plaintext, password, nBits):
    printDBG( 'encrypt begin ' )
    blockSize = 16
    if not nBits in (128, 192, 256): return ""
#    plaintext = plaintext.encode("utf-8")
#    password  = password.encode("utf-8")
    nBytes = nBits//8
    pwBytes = [0] * nBytes
    for i in range(nBytes): pwBytes[i] = 0 if i>=len(password) else ord(password[i])
    key = Cipher(pwBytes, KeyExpansion(pwBytes))
    key += key[:nBytes-16]

    counterBlock = [0] * blockSize
    now = datetime.datetime.now()
    nonce = time.mktime( now.timetuple() )*1000 + now.microsecond//1000
    nonceSec = int(nonce // 1000)
    nonceMs  = int(nonce % 1000)

    for i in range(4): counterBlock[i] = urs(nonceSec, i*8) & 0xff
    for i in range(4): counterBlock[i+4] = nonceMs & 0xff

    ctrTxt = ""
    for i in range(8): ctrTxt += chr(counterBlock[i])

    keySchedule = KeyExpansion(key)

    blockCount = int(math.ceil(float(len(plaintext))/float(blockSize)))
    ciphertxt = [0] * blockCount

    for b in range(blockCount):
        for c in range(4): counterBlock[15-c] = urs(b, c*8) & 0xff
        for c in range(4): counterBlock[15-c-4] = urs(b/0x100000000, c*8)

        cipherCntr = Cipher(counterBlock, keySchedule)

        blockLength = blockSize if b<blockCount-1 else (len(plaintext)-1)%blockSize+1
        cipherChar = [0] * blockLength

        for i in range(blockLength):
            cipherChar[i] = cipherCntr[i] ^ ord(plaintext[b*blockSize+i])
            cipherChar[i] = chr( cipherChar[i] )
        ciphertxt[b] = ''.join(cipherChar)

    ciphertext = ctrTxt + ''.join(ciphertxt)
    ciphertext = base64.b64encode(ciphertext)

    return ciphertext

def urs(a, b):
    printDBG( 'urs begin ' )
    a &= 0xffffffff
    b &= 0x1f
    if a&0x80000000 and b>0:
        a = (a>>1) & 0x7fffffff
        a = a >> (b-1)
    else:
        a = (a >> b)
    return a
