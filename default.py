#!/usr/bin/env python
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

#######################################
#   LIBRARIES & GLOBALS DECLARATIONS
#######################################
# Python libraries
import sys, re, os
from urlparse import urlparse, parse_qs, urljoin
from itertools import chain
from datetime import datetime, date
import time
import urllib2
from traceback import print_exc

# json
try:
    import json
except:
    import simplejson as json  # @UnresolvedImport

# Beautiful Soup
from BeautifulSoup import BeautifulSoup as BS

# XBMC includes
import xbmcgui
import xbmc
import xbmcaddon

# DEBUG
REMOTE_DBG = False

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        sys.path.append(r'C:\eclipse\plugins\org.python.pydev_3.8.0.201409251235\pysrc')
        xbmc.log('PYTHONPATH:' + str(sys.path)) 
        import pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)

#######################
#   GLOBALS Definition
#######################
__addon__         = xbmcaddon.Addon('script.slbenfica')
__language__      = __addon__.getLocalizedString
__addon_path__    = __addon__.getAddonInfo('path').decode("utf-8")
__addon_name__    = __addon__.getAddonInfo('name')
__addon_id__      = __addon__.getAddonInfo('id')
__author__        = __addon__.getAddonInfo('author')
__version__       = __addon__.getAddonInfo('version')
__resource__      = xbmc.translatePath(os.path.join(__addon_path__, 'resources', 'lib').encode("utf-8")).decode("utf-8")
__addon_icon__    = xbmc.translatePath(os.path.join( __addon_path__, "icon.png")).decode('utf-8')
__settings_file__ = os.path.join(__resource__, "settings.xml").replace("\\\\","\\")
__temp_folder__   = os.path.join(__resource__, "temp" ).decode( "utf-8" )
__imagepath__     = os.path.join(__resource__,"skins", "Default", "media").decode( "utf-8" )
__datapath__      = os.path.join(xbmc.translatePath('special://masterprofile/addon_data/').decode('utf-8'), __addon_id__)
__profilepath__   = os.path.join(xbmc.translatePath('special://profile/addon_data/').decode('utf-8'), __addon_id__)
__preamble__      = '[SL Benfica]'
#__logdebug__      = __addon__.getSetting("logging") 

#####################
#    PATH INCLUDE
#####################
sys.path = [__resource__] + sys.path

#####################
#     GUI CLASS
#####################
from gui import GUI
#####################
#     LOG CLASS
#####################
from xlogger import Logger

lw = Logger(preamble=__preamble__)

try:
    __lang__ = xbmc.getLanguage(xbmc.ISO_639_1, False) # Gotham @UndefinedVariable
except: 
    __lang__ = xbmc.getLanguage() # Frodo @UndefinedVariable
    if   __lang__ == 'Portuguese': __lang__ = 'pt'
    elif __lang__ == 'Spanish':    __lang__ = 'es'
    else: __lang__ = 'en'

if __lang__ == "pt": 
    LANG = "pt-PT"
elif __lang__ == "es":
    LANG = "es-ES"
else:
    LANG = "en-US"

#######################
#   Base URLs
#######################
#   TYPES:
###########################################
#   {media_type} = videos | fotos
#   {lang}       = pt-pt  | es-es | en-us
###########################################

BASE_URL     = 'http://www.slbenfica.pt/'
HOME_URL     = 'http://www.slbenfica.pt/{lang}/home.aspx'.format(lang=LANG)
VIDEOS_URL   = 'http://www.slbenfica.pt/{lang}/videos.aspx'.format(lang=LANG)
PHOTOS_URL   = 'http://www.slbenfica.pt/{lang}/fotos.aspx'.format(lang=LANG)
VIDEOS_CATEGORY_URL = 'http://www.slbenfica.pt/videos/albuns/tabid/2805/LCmid/9435/filter-Page/{page}/cat/{cat_id}/filter-eType/all/filter-Tags/all/sort-Asc/default/sort-Desc/default/language/{lang}/Default.aspx'
PHOTOS_CATEGORY_URL = 'http://www.slbenfica.pt/fotos/albuns/tabid/2802/LCmid/9751/filter-Page/{page}/cat/{cat_id}/filter-eType/all/filter-Tags/all/sort-Asc/default/sort-Desc/default/language/{lang}/Default.aspx'
VIDEOS_ALBUM_URL    = 'http://www.slbenfica.pt/video/detalhealbum/tabid/2806/cat/{album_id}/language/{lang}/Default.aspx'
PHOTOS_ALBUM_URL    = 'http://www.slbenfica.pt/fotos/detalhealbum/tabid/2803/cat/{album_id}/language/{lang}/Default.aspx'
YOUTUBE_URL  = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid={id}'

#######################
#   Base Functions
#######################

def _unicode(text, encoding='utf-8'):
    try: text = unicode(text, encoding)
    except: pass
    return text

def normalize(d, key = None, default = ""):
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

def _full_url(url):
    ''' Retrieve full url '''
    return urljoin(BASE_URL, url)

def _html(url):
    '''Downloads the resource at the given url and parses via BeautifulSoup'''
    return BS(download_page(url), convertEntities=BS.HTML_ENTITIES)

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

def get_cat_id(url, otype):

    if   otype == 'category': pattern = '/albuns/tabid/.*?/cat/(.*?)/language/'
    elif otype == 'album': pattern = '/detalhealbum/tabid/.*?/cat/(.*?)/language/'

    match = re.search(pattern, url)
    
    return match.group(1)

def find_previous_next_page(page_html):

    prev_page = page_html.find('a', {'class': 'ic_arrow_prev'})
    next_page = page_html.find('a', {'class': 'ic_arrow_next'})
    
    if prev_page: prev_page_url = True
    else: prev_page_url = False
    if next_page: next_page_url = True
    else: next_page_url = False

    return prev_page_url, next_page_url

#########################
#   Slideshow methods
#########################
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


############################
#           MAIN
############################

#if __name__ == '__main__': 
#    plugin.run()
if ( __name__ == "__main__" ):
    
    if xbmcgui.Window( 10000 ).getProperty( "slbenfica_addon_running" ) == "True":
        lw.log(["SL Benfica Addon already running, exiting..."], xbmc.LOGNOTICE )
    else:
        xbmcgui.Window( 10000 ).setProperty( "slbenfica_addon_running", "True" )
    try:
        lw.log( ["############################################################"], xbmc.LOGNOTICE )
        lw.log( ["#    %-50s    #" % __addon_name__], xbmc.LOGNOTICE )
        lw.log( ["#        default.py module                                 #"], xbmc.LOGNOTICE )
        lw.log( ["#    %-50s    #" % __addon_id__], xbmc.LOGNOTICE )
        lw.log( ["#    %-50s    #" % __author__], xbmc.LOGNOTICE )
        lw.log( ["#    %-50s    #" % __version__], xbmc.LOGNOTICE )
        lw.log( ["############################################################"], xbmc.LOGNOTICE )

        window = GUI( "script-slbenfica.xml" , __addon_path__, "Default")
        window.doModal()
        del window
    except:
        lw.log(['Error in script occured:', print_exc()])
        

############################