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
import re, urllib    
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.config import config, ConfigSelection, ConfigYesNo, ConfigText, getConfigListEntry, ConfigPIN
###################################################

###################################################
# Config options for HOST
###################################################
#config.plugins.iptvplayer.PIN = ConfigPIN(default = 6666 , censor='*')

def GetConfigList():
    optionList = []
    #optionList.append(getConfigListEntry("PIN:", config.plugins.iptvplayer.PIN))
    return optionList
###################################################

###################################################
# Title of HOST
###################################################
def gettytul():
    return 'XXX'

###################################################
# Get PIN possible
###################################################
def getpin():
    return True


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
    currList = []
    MAIN_URL = ''

    def __init__(self):
        printDBG( 'Host __init__ begin' )
        self.cm = pCommon.common()
        self.currList = []
        printDBG( 'Host __init__ begin' )
        
    def setCurrList(self, list):
        printDBG( 'Host setCurrList begin' )
        self.currList = list
        printDBG( 'Host setCurrList begin' )
        return 

    def getInitList(self):
        printDBG( 'Host getInitList begin' )
        #self.currList = self.MAIN_MENU
        self.currList = self.listsItems(-1, 'http://m.tube8.com', 'main-menu')
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
        valTab = []
        if name == 'main-menu':
           printDBG( 'Host listsItems begin name='+name )
           valTab.append(CDisplayListItem('tube8.com',   'm.tube8.com',        CDisplayListItem.TYPE_CATEGORY, ['http://m.tube8.com'],        'tube8',   'http://cdn1.static.tube8.phncdn.com/images/t8logo.png', None)) 
           valTab.append(CDisplayListItem('youporn.com', 'mobile.youporn.com', CDisplayListItem.TYPE_CATEGORY, ['http://mobile.youporn.com'], 'youporn', 'http://cdn1.static.youporn.phncdn.com/cb/bundles/youpornwebfront/images/l_youporn_black.png', None)) 
           valTab.append(CDisplayListItem('pornhub.com', 'm.pornhub.com',      CDisplayListItem.TYPE_CATEGORY, ['http://m.pornhub.com'],      'pornhub', 'http://cdn1.static.pornhub.phncdn.com/images/pornhub_logo.png', None)) 
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'tube8':
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://m.tube8.com' 
           valTab.append(CDisplayListItem('LAST',       'Last',       CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL],                    'tube8-last', '', None)) 
           valTab.append(CDisplayListItem('CATEGORIES', 'Categories', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+'/category/browse'], 'tube8-categories', '', None)) 
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'youporn':
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://mobile.youporn.com' 
           valTab.append(CDisplayListItem('LAST',       'Last',       CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL],                    'youporn-last', '', None)) 
           valTab.append(CDisplayListItem('CATEGORIES', 'Categories', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+'/category/browse'], 'youporn-categories', '', None)) 
           printDBG( 'Host listsItems end' )
           return valTab
        if name == 'pornhub':
           printDBG( 'Host listsItems begin name='+name )
           self.MAIN_URL = 'http://m.pornhub.com' 
           valTab.append(CDisplayListItem('LAST',       'Last',       CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL],                    'pornhub-last', '', None)) 
           valTab.append(CDisplayListItem('CATEGORIES', 'Categories', CDisplayListItem.TYPE_CATEGORY, [self.MAIN_URL+'/category/browse'], 'pornhub-categories', '', None)) 
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

        return valTab

    def getResolvedURL(self, url):
        printDBG( 'Host getResolvedURL begin' )
        videoUrl = ''
        valTab = []
        query_data = {'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True}
        try:
           data = self.cm.getURLRequestData(query_data)
           #printDBG( 'Host getResolvedURL data: '+data )
        except:
           printDBG( 'Host getResolvedURL query error' )
           return videoUrl
        
        if self.MAIN_URL == 'http://m.tube8.com':
           match = re.compile('<div class="play_video.+?<a href="(.+?)"', re.DOTALL).findall(data)
        if self.MAIN_URL == 'http://mobile.youporn.com':
           match = re.compile('<div class="play_video.+?<a href="(.+?)"', re.DOTALL).findall(data)
        if self.MAIN_URL == 'http://m.pornhub.com':
           #printDBG( 'Host getResolvedURL data: '+data )
           match = re.compile('<div class="play_video.+?<a href="(.+?)"', re.DOTALL).findall(data)
            
        if len(match)>0:
           videoUrl = match[0]
        printDBG( 'Host getResolvedURL end' )
        return videoUrl
