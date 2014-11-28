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
from urlparse import urlparse, parse_qs, urljoin, urlsplit, urlunsplit
from itertools import chain
from datetime import datetime, date
import time
from urllib import quote, unquote, urlencode
import urllib2
import requests
import xbmc, xbmcaddon, xbmcplugin

try:
    import json
except:
    import simplejson as json

# Beautiful Soup
import html5lib
import six
from bs4 import BeautifulSoup, NavigableString, Tag
from cookielib import CookieJar

#-----------------------------------
#   Utils Methods
#-----------------------------------
def swap_dictionary(original_dict):
    return dict([(v, k) for (k, v) in original_dict.iteritems()])

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
    __libs__          = os.path.join(__resource__, 'lib/').decode( 'utf-8' )
    __mediapath__     = os.path.join(__resource__,'skins/', 'Default', 'media').decode( "utf-8" )
    __imagespath__    = os.path.join(__resource__,'images').decode( "utf-8" )
    __datapath__      = os.path.join(xbmc.translatePath('special://masterprofile/addon_data/').decode('utf-8'), __id__)
    __profilepath__   = os.path.join(xbmc.translatePath('special://profile/addon_data/').decode('utf-8'), __id__)
    __preamble__      = '[SL Benfica]'    
    #__logdebug__      = __addon__.getSetting("logging") 

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

#-------------------
#  Controls IDs
#-------------------
class Controls:
    #--------------
    #   BUTTONS
    #--------------
    MAIN_MENU_CLUB_BUTTON                   = 110
    MAIN_MENU_NEWS_BUTTON                   = 120
    MAIN_MENU_VIDEOS_BUTTON                 = 130
    MAIN_MENU_PHOTOS_BUTTON                 = 140
    MAIN_MENU_STADIUM_BUTTON                = 150
    MAIN_MENU_TICKETS_BUTTON                = 160
    MAIN_MENU_CALENDAR_BUTTON               = 170
    MAIN_MENU_SPORTS_BTN                    = 180 
    MAIN_MENU_LIVE_MATCH_BTN                = 190
    MAIN_MENU_EXIT_BTN                      = 200
    CLUB_MENU_INFO_BTN                      = 111
    CLUB_MENU_STRUCTURE_BTN                 = 112
    CLUB_MENU_HISTORY_BTN                   = 113
    CLUB_MENU_MUSEUM_BTN                    = 114
    NEWS_MENU_HEADLINES_BTN                 = 121
    NEWS_MENU_SPORTS_BTN                    = 122
    STADIUM_MENU_LIGHT_BTN                  = 151
    STADIUM_MENU_INFO_BTN                   = 152
    STADIUM_MENU_TOURS_BTN                  = 153
    STADIUM_MENU_VIRTUAL_BTN                = 154
    TICKETS_MENU_MATCHES_BTN                = 161
    TICKETS_MENU_MATCHES_BTN                = 162
    CALENDAR_MENU_TODAY_BTN                 = 171
    CALENDAR_MENU_WEEKLY_BTN                = 172
    CALENDAR_MENU_MONTHLY_BTN               = 173
    CALENDAR_NEXT_MATCHES_NEXT_BTN          = 174
    CALENDAR_NEXT_MATCHES_PREV_BTN          = 175
    #--------------
    #   CONTENT
    #--------------        
    # CLUB      
    CONTENT_CLUB_PANEL                      = 9010
    CONTENT_CLUB_INFO_PANEL                 = 9011
    CONTENT_CLUB_STRUCTURE_PANEL            = 9012
    CONTENT_CLUB_HISTORY_PANEL              = 9013
    CONTENT_CLUB_MUSEUM_PANEL               = 9014
    # NEWS      
    CONTENT_NEWS_HEADLINES_PANEL            = 9020
    CONTENT_NEWS_SPORTS_PANEL               = 9021
    CONTENT_NEWS_SPORT_PANEL                = 9022
    CONTENT_NEWS_ARTICLE_PANEL              = 9023
    # VIDEOS        
    CONTENT_VIDEOS_SPORTS_PANEL             = 9030
    CONTENT_VIDEOS_SPORTS_LIST              = 9031
    CONTENT_VIDEOS_SPORT_ALBUMS_PANEL       = 9032
    CONTENT_VIDEOS_SPORT_ALBUMS_LIST        = 9033
    CONTENT_ALBUMS_VIDEOS_PANEL             = 9034
    CONTENT_ALBUMS_VIDEOS_LIST              = 9035
    # PHOTOS        
    CONTENT_PHOTOS_SPORTS_PANEL             = 9040
    CONTENT_PHOTOS_SPORTS_LIST              = 9041
    CONTENT_PHOTOS_SPORT_ALBUMS_PANEL       = 9042
    CONTENT_PHOTOS_SPORT_ALBUMS_LIST        = 9043
    CONTENT_SLIDESHOW_PANEL                 = 9044
    CONTENT_SLIDESHOW_LIST                  = 9045
    # STADIUM       
    CONTENT_STADIUM_PANEL                   = 9050
    CONTENT_STADIUM_INFO_PANEL              = 9051
    CONTENT_STADIUM_TOURS_PANEL             = 9052
    CONTENT_STADIUM_VIRTUAL_PANEL           = 9053
    # TICKETS       
    CONTENT_TICKETS_MATCHES_PANEL           = 9060
    CONTENT_TICKETS_MUSEUM_PANEL            = 9061
    # CALENDAR
    CONTENT_CALENDAR_NEXT_MATCHES_PANEL     = 9070
    CONTENT_CALENDAR_TODAY_PANEL            = 9071
    CONTENT_CALENDAR_WEEKLY_PANEL           = 9072
    CONTENT_CALENDAR_MONTHLY_PANEL          = 9073
    CONTENT_CALENDAR_SPORTS_PANEL           = 9074
    CONTENT_CALENDAR_SPORT_EVENTS_PANEL     = 9075
    CONTENT_CALENDAR_NEXT_MATCHES_LIST      = 9076
    # SPORTS
    CONTENT_SPORTS_PANEL                    = 9080
    CONTENT_SPORTS_INFO_PANEL               = 9081
    CONTENT_SPORTS_INFO_DATA_PANEL          = 9082
    # LIVE MATCHES
    CONTENT_LIVE_MATCHES_CONTAINER_PANEL    = 9090
    CONTENT_LIVE_MATCHES_PANEL              = 9091
    CONTENT_LIVE_MATCHES_LIST_PANEL         = 9092
    # PANEL
    CONTENT_PANEL_PANEL                     = 9100


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
def BS(url, proxies={}):

    proxies = {'http': 'http://peu141:Glorioso1904@ep-proxy.bportugal.pt:8080', 
               'https': 'http://peu141:Glorioso1904@ep-proxy.bportugal.pt:8080'}

    r = requests.get(url, proxies=proxies)
    return BeautifulSoup(r.text, 'html5lib')

def _full_url(root, url):
    return fixurl(urljoin(root, url))

def fixurl(url):
    # turn string into unicode
    if not isinstance(url,unicode):
        url = url.decode('utf8')
    # parse it
    parsed = urlsplit(url)
    # divide the netloc further
    userpass,at,hostport = parsed.netloc.rpartition('@')
    user,colon1,pass_ = userpass.partition(':')
    host,colon2,port = hostport.partition(':')
    # encode each component
    scheme = parsed.scheme.encode('utf8')
    user = quote(user.encode('utf8'))
    colon1 = colon1.encode('utf8')
    pass_ = quote(pass_.encode('utf8'))
    at = at.encode('utf8')
    host = host.encode('idna')
    colon2 = colon2.encode('utf8')
    port = port.encode('utf8')
    path = '/'.join(  # could be encoded slashes!
        quote(unquote(pce).encode('utf8'),'')
        for pce in parsed.path.split('/'))
    query = quote(unquote(parsed.query).encode('utf8'),'=&?/')
    fragment = quote(unquote(parsed.fragment).encode('utf8'))
    # put it back together
    netloc = ''.join((user,colon1,pass_,at,host,colon2,port))
    return urlunsplit((scheme,netloc,path,query,fragment))

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

def raw_string(s):
    if isinstance(s, str): 
        s = s.encode('string-escape')
    elif isinstance(s, unicode): 
        s = s.encode('unicode-escape')
    return s

#----------------------
#     COLORS
#----------------------
def kodi_color(color):
    try:
        return{'white':  'FFFFFFFF',
               'blue':   'FF0000FF',
               'cyan':   'FF00FFFF',
               'violet': 'FFEE82EE',
               'pink':   'FFFF1493',
               'red':    'FFFF0000',
               'green':  'FF00FF00',
               'yellow': 'FFFFFF00',
               'orange': 'FFFF4500'
               }[color]
    except:
        return 'FFFFFFFF'

def set_coloring(text, string, color):
    return text.replace(string, set_color(string, color))

def set_color(string, color):
    color = kodi_color(color)
    return '[COLOR=%s]%s[/COLOR]' % (color, string)

def clean_color(text):
    return re.sub(r'\W+\[*COLOR.*?\]', '', text)

def set_bold(string, replace=False):
    if replace:
        for tag in ['<strong>', '<b>']:
            string = string.replace(tag, r'[B]')
        for tag in ['</strong>', '</b>']:
            string = string.replace(tag, r'[/B]')
    else: 
        string = "[B]%s[/B]" % (string)
    return string

def set_bold_text(text, string, replace=False):
    return text.replace(string, set_bold(string, replace))

def set_italic(string, replace=False):
    if replace:
        italic_string = string.replace('<i>', '[I]').replace('</i>', r'[/I]')
    else:
        italic_string = "[I]%s[/I]" % (string)
    return italic_string

def set_italic_text(text, string, replace=False):
    return text.replace(string, set_italic(string, replace))

def replace_nbsp(text):
    if isinstance(text, Tag):
        for p in text.find_all('p'):
            if p.string == u'\xa0':
                p.string = r'[CR]'
    return text

def replace_br(text, func=None):
    if isinstance(text, Tag):
        for br in text.find_all('br'):
            if br.parent.name == 'p': # <br /> enclosed inside p tag. replace only
                br.parent.string = r'[CR]'
            else:
                br.string = r'[CR]'
                br.name = 'p'
    return text

def kodi_titles(text, color):
    if isinstance(text, Tag) or isinstance(text, BeautifulSoup):
        tags = ['h1', 'h2', 'h3']
        for tag in tags:
            for tag_ in text.find_all(tag):
                tag_.string = set_bold(set_color(tag_.string, color))
    return text

def kodi_text(text, func=None):
    if isinstance(text, Tag):
        kodi_text = [line for line in text.stripped_strings]
    elif type(text) == list:
        if func:
            kodi_text = [line for line in filter(func, text)]
        else:
            kodi_text = [line for line in text]
    else: return text # string
    text = r'[CR]'.join(kodi_text).encode('utf-8')
    patterns = []
    iter = re.finditer('(\[CR\]){3,}', text)
    if iter:
        for match in iter:
            pattern = raw_string(text[match.start():match.end()])
            patterns.append(pattern)
        if patterns:
            patterns.sort(key = lambda s: len(s))
            for p in patterns:
                final_text = text.replace(raw_string(p), r'[CR][CR]')
            return final_text.decode('utf-8')
    return text.decode('utf-8')

def stringify_text(text, func=None):
    if isinstance(text, Tag):
        stringify_text = [line.strip() for line in text.stripped_strings]
    elif type(text) == list:
        if func:
            stringify_text = [line.strip() for line in filter(func, text)]
        else:
            stringify_text = [line.strip() for line in text]
    else: return text # string
    return u'\n'.join(stringify_text)

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