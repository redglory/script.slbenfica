# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 redglory | sript.slbenfica
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#-----------------------
#  Common Includes
#-----------------------
import sys, re, os
from urlparse import urlparse, parse_qs, urljoin
from itertools import chain
from datetime import datetime, date
import time
import urllib2
import xbmc, xbmcaddon, xbmcplugin

try:
    import json
except:
    import simplejson as json

# Beautiful Soup
from BeautifulSoup import BeautifulSoup as BS


#-----------------------------------
#   Addon Globals & Methods
#-----------------------------------
class Addon:
    __addon__         = xbmcaddon.Addon('script.slbenfica')
    __translate__     = __addon__.getLocalizedString
    __language__      = xbmc.getLanguage(1) #[language] - two letter language
    __path__          = __addon__.getAddonInfo('path').decode("utf-8")
    __name__          = __addon__.getAddonInfo('name')
    __id__            = __addon__.getAddonInfo('id')
    __icon__          = __addon__.getAddonInfo('icon')
    __author__        = __addon__.getAddonInfo('author')
    __version__       = __addon__.getAddonInfo('version')
    __resource__      = xbmc.translatePath(os.path.join(__path__, 'resources').encode('utf-8')).decode('utf-8')
    __libs__          = os.path.join(__resource__, 'lib').decode( 'utf-8' )
    __mediapath__     = os.path.join(__resource__,'skins', 'Default', 'media').decode( "utf-8" )
    __imagespath__    = os.path.join(__resource__,'images').decode( "utf-8" )
    __datapath__      = os.path.join(xbmc.translatePath('special://masterprofile/addon_data/').decode('utf-8'), __id__)
    __profilepath__   = os.path.join(xbmc.translatePath('special://profile/addon_data/').decode('utf-8'), __id__)
    __preamble__      = '[SL Benfica]'    
    #__logdebug__      = __addon__.getSetting("logging") 

#----------------------
#     LOG CLASS
#----------------------
from xlogger import Logger

global lw

lw = Logger(preamble=Addon.__preamble__)

#------------------------
#     Addon methods
#------------------------
def _get_language(lang=Addon.__language__):
    
    try:
        return{'pt': 'pt-PT',
               'es': 'es-ES',
               'en': 'en-US'
              }[lang]
    except:
        return 'en-US'

def getSetting(name):
    return Addon.__addon__.getSetting(name)

def setSetting(name, value):
    Addon.__addon__.setSetting(id=name, value=value)

def showNotification(title, message, timeout=2000, icon=Addon.__icon__):
    def clean(s):
        return str(s.encode('utf-8', 'ignore'))
    command = ''
    if icon:
        command = 'Notification(%s,%s,%s,%s)' % (clean(title), clean(message), timeout, icon)
    else:
        command = 'Notification(%s,%s,%s)' % (clean(title), clean(message), timeout)
    xbmc.executebuiltin(command)

def runPlugin(url):
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')


#------------------------
#  Web related methods
#------------------------
def download_page(url, data=None):
    
    request = urllib2.Request(url, data)
    request.add_header('Accept-Encoding', 'utf-8')
    response = urllib2.urlopen(request)
    return response

def _full_url(root, url):
    return urljoin(root, url)

def _html(url):
    return BS(download_page(url))


#---------------------------
#  Date and String methods
#---------------------------
def monthToNum(month):

    return{
            'Jan' : 1,
            'Fev' : 2,
            'Mar' : 3,
            'Abr' : 4,
            'Mai' : 5,
            'Jun' : 6,
            'Jul' : 7,
            'Ago' : 8,
            'Set' : 9, 
            'Out' : 10,
            'Nov' : 11,
            'Dez' : 12
    }[month.title()]

def _unicode(text, encoding='utf-8'):
    try: text = unicode(text, encoding)
    except: pass
    return text

def _normalize(d, key = None, default = ""):
    if key is None:
        text = d
    else:
        text = d.get(key, default)
        if not text:
            return text
    try:
        text = unicodedata.normalize('NFKD', _unicode(text)).encode('ascii', 'ignore')
    except:
        pass
    return text

def remove_accents(name):
    return unicodedata.normalize('NFKD', name).encode('ascii','ignore').lower()    

def convert_date(date_str, input_format, output_format):
    """
    Examples:
    - INPUT: convert_date('2012-07-18 10:03:19', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y')
    - OUTPUT: 18-07-2013
    -----------------------
    - INPUT: convert_date('01-01-2014', '%d-%m-%Y', '%Y-%m-%d')
    - OUTPUT: 2014-01-01
    """
    try:
        d = datetime.strptime(date_str, input_format)
    except TypeError:
        d = datetime(*(time.strptime(date_str, input_format)[0:6]))

        return d.strftime(output_format)


#------------------------
#     Player methods
#------------------------
def resolve_youtube_url(youtube_url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """

    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return YOUTUBE_URL.format(id=str(query.path[1:]))
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return YOUTUBE_URL.format(id=str(p['v'][0]))
        if query.path[:7] == '/embed/':
            return YOUTUBE_URL.format(id=str(query.path.split('/')[2]))
        if query.path[:3] == '/v/':
            return YOUTUBE_URL.format(id=str(query.path.split('/')[2]))
    # fail?
    return None

# add item with youtube video path
def play_video(youtube_url):

    youtube_plugin_url = resolve_youtube_url(youtube_url)

    if youtube_plugin_url:
        item = xbmcgui.ListItem(path=youtube_plugin_url) 
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


#------------------------
#   Slideshow methods
#------------------------
def clear_slideshow():
    get_players = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'))  # @UndefinedVariable
    for _player in get_players['result']:
        if _player['type'] == 'picture':
            stop_slideshow = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.Stop", "params": {"playerid":%i}, "id": 1}' % _player['playerid'])  # @UndefinedVariable
        else: continue
    clear_playlist = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": {"playlistid":2}, "id": 1}')  # @UndefinedVariable


def add_playlist(images):
    items = []
    for image in images:
        item = '{"jsonrpc": "2.0", "method": "Playlist.Add", "params": {"playlistid": 2, "item": {"file" : "%s"}}, "id": 1}' % image['path'] 
        add_item = items.append(item.encode('ascii'))
    print 'Adding - %s images' %str(len(items))
    if len(items) > 0:
        add_playlist = xbmc.executeJSONRPC(str(items).replace("'",""))  # @UndefinedVariable

def start_slideshow(images):

    print 'Slideshow Images = '+ str(len(images))
    if len(images) > 0:
        clear_slideshow()
        add_playlist(images)
        get_playlist = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.GetItems", "params": {"playlistid":2}, "id": 1}'))  # @UndefinedVariable
        if get_playlist['result']['limits']['total'] > 0:
            get_players = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'))  # @UndefinedVariable
            pic_player = False
            for _player in get_players['result']:
                if _player['type'] == 'picture':
                    pic_player = True
                else: continue
            if not pic_player:
                play = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.Open","params":{"item":{"playlistid":2}} }')  # @UndefinedVariable
    else:
        clear_slideshow()

#-------------------
#  Script Modes
#-------------------
class Mode:
    UPDATE = 0
    VIEW = 1
    PLAY = 2
    QUEUE = 3
    DOWNLOAD = 4
    EXECUTE = 5
    ADDTOFAVOURITES = 6
    REMOVEFROMFAVOURITES = 7
    EDITITEM = 8
    ADDITEM = 9
    DOWNLOADCUSTOMMODULE = 10
    REMOVEFROMCUSTOMMODULES = 11
    INSTALLADDON = 12
