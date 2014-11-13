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
from urllib import quote, unquote
import urllib2
import xbmc, xbmcaddon, xbmcplugin

try:
    import json
except:
    import simplejson as json

# Beautiful Soup
import html5lib
import six
from bs4 import BeautifulSoup

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
    __libs__          = os.path.join(__resource__, 'lib').decode( 'utf-8' )
    __mediapath__     = os.path.join(__resource__,'skins', 'Default', 'media').decode( "utf-8" )
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
    VIDEOS_MENU_FOOTBALL_BTN                = 131
    VIDEOS_FOOTBALL_YOUTH_TEAMS_BTN         = 231
    VIDEOS_FOOTBALL__B_TEAM_BTN             = 232
    VIDEOS_MENU_FUTSAL_BTN                  = 132
    VIDEOS_MENU_HOCKEY_BTN                  = 133
    VIDEOS_MENU_BASKETBALL_BTN              = 134
    VIDEOS_MENU_HANDBALL_BTN                = 135
    VIDEOS_MENU_VOLLEYBALL_BTN              = 136
    VIDEOS_MENU_ATHLETICS_BTN               = 137
    VIDEOS_MENU_CLUB_BTN                    = 138
    VIDEOS_MENU_OLYMPIC_BTN                 = 139
    VIDEOS_MENU_OTHERS_BTN                  = 230
    PHOTOS_MENU_FOOTBALL_BTN                = 141
    PHOTOS_FOOTBALL_FIRST_TEAM_BTN          = 243
    PHOTOS_FOOTBALL_YOUTH_TEAMS_BTN         = 244
    PHOTOS_FOOTBALL_B_TEAM_BTN              = 245
    PHOTOS_FOOTBALL_GENERATIONS_BTN         = 246
    PHOTOS_MENU_FUTSAL_BTN                  = 142
    PHOTOS_MENU_HOCKEY_BTN                  = 143
    PHOTOS_HOCKEY_FEMALE_BTN                = 247
    PHOTOS_MENU_BASKETBALL_BTN              = 144
    PHOTOS_MENU_HANDBALL_BTN                = 145
    PHOTOS_MENU_VOLLEYBALL_BTN              = 146
    PHOTOS_MENU_ATHLETICS_BTN               = 147
    PHOTOS_MENU_GOLF_BTN                    = 148
    PHOTOS_MENU_JUDO_BTN                    = 149
    PHOTOS_MENU_RUGBY_BTN                   = 240
    PHOTOS_RUGBY_FEM_BTN                    = 248
    PHOTOS_MENU_CLUB_BTN                    = 241
    PHOTOS_CLUB_FAMILY_BTN                  = 249
    PHOTOS_MENU_OLYMPIC_BTN                 = 242
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
    CONTENT_CLUB_VIEW                       = 9010
    CONTENT_CLUB_INFO_VIEW                  = 9011
    CONTENT_CLUB_STRUCTURE_VIEW             = 9012
    CONTENT_CLUB_HISTORY_VIEW               = 9013
    CONTENT_CLUB_MUSEUM_VIEW                = 9014
    # NEWS      
    CONTENT_NEWS_HEADLINES_VIEW             = 9020
    CONTENT_NEWS_SPORTS_VIEW                = 9021
    CONTENT_NEWS_SPORT_VIEW                 = 9022
    CONTENT_NEWS_ARTICLE_VIEW               = 9023
    # VIDEOS        
    CONTENT_VIDEOS_SPORTS_VIEW              = 9031
    CONTENT_VIDEOS_ALBUMS_VIEW              = 9032
    CONTENT_ALBUMS_VIDEOS_VIEW              = 9033
    # PHOTOS        
    CONTENT_PHOTOS_SPORTS_VIEW              = 9044
    CONTENT_PHOTOS_ALBUMS_VIEW              = 9045
    CONTENT_SLIDESHOW_VIEW                  = 9046
    # STADIUM       
    CONTENT_STADIUM_LIGHT_VIEW              = 9050
    CONTENT_STADIUM_INFO_VIEW               = 9051
    CONTENT_STADIUM_TOURS_VIEW              = 9052
    CONTENT_STADIUM_VIRTUAL_VIEW            = 9053
    # TICKETS       
    CONTENT_TICKETS_MATCHES_VIEW            = 9060
    CONTENT_TICKETS_MUSEUM_VIEW             = 9061
    # CALENDAR
    CONTENT_CALENDAR_NEXT_MATCHES_VIEW      = 9070
    CONTENT_CALENDAR_TODAY_VIEW             = 9071
    CONTENT_CALENDAR_WEEKLY_VIEW            = 9072
    CONTENT_CALENDAR_MONTHLY_VIEW           = 9073
    CONTENT_CALENDAR_SPORTS_VIEW            = 9074
    CONTENT_CALENDAR_SPORT_EVENTS_VIEW      = 9075
    CONTENT_CALENDAR_NEXT_MATCHES_LIST      = 9076
    # SPORTS
    CONTENT_SPORTS_VIEW                     = 9080
    CONTENT_SPORTS_INFO_VIEW                = 9081
    CONTENT_SPORTS_INFO_DATA_VIEW           = 9082
    # LIVE MATCHES
    CONTENT_LIVE_MATCHES_CONTAINER_VIEW     = 9090
    CONTENT_LIVE_MATCHES_VIEW               = 9091
    CONTENT_LIVE_MATCHES_LIST_VIEW          = 9092
    # PANEL
    CONTENT_PANEL_VIEW                      = 9100

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
    return BeautifulSoup(download_page(url), 'html5lib')


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

def kodi_text(text):
    pretty_text = [line for line in text.stripped_strings]
    return u'\n'.encode('utf-8').join(pretty_text)

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
        for pce in parsed.path.split('/')
    )
    query = quote(unquote(parsed.query).encode('utf8'),'=&?/')
    fragment = quote(unquote(parsed.fragment).encode('utf8'))

    # put it back together
    netloc = ''.join((user,colon1,pass_,at,host,colon2,port))
    return urlunsplit((scheme,netloc,path,query,fragment))    

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