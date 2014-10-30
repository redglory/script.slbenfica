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
import sys, re
from urlparse import urlparse, parse_qs, urljoin
from itertools import chain
from datetime import datetime, date
import time
import urllib2
from traceback import print_exc

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
import gui

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
__addon__            = xbmcaddon.Addon('script.slbenfica')
__language__         = __addon__.getLocalizedString
__addon_path__       = __addon__.getAddonInfo('path').decode("utf-8")
__addon_name__       = __addon__.getAddonInfo('name')
__addon_id__         = __addon__.getAddonInfo('id')
__author__           = __addon__.getAddonInfo('author')
__version__          = __addon__.getAddonInfo('version')
__resource__         = xbmc.translatePath(os.path.join(__addon_path__, 'resources', 'lib').encode("utf-8")).decode("utf-8")
__addon_icon__       = xbmc.translatePath(os.path.join( __addon_path__, "icon.png")).decode('utf-8')
__settings_file__    = os.path.join(__resource__, "settings.xml").replace("\\\\","\\")
__temp_folder__      = os.path.join(__resource__, "temp" ).decode( "utf-8" )
__imagepath__        = os.path.join(__resource__,"skins", "Default", "media").decode( "utf-8" )
__datapath__         = os.path.join(xbmc.translatePath('special://masterprofile/addon_data/').decode('utf-8'), __addon_id__)
__profilepath__      = os.path.join(xbmc.translatePath('special://profile/addon_data/').decode('utf-8'), __addon_id__)

MAX_INFO_LOG_LEVEL = 1
MAX_DEBUG_LOG_LEVEL = 2

sys.path = [__resource__] + sys.path

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

# if level <= 0, sends LOGERROR msg.  For positive values, sends LOGNOTICE
# if level <= MAX_INFO_LOG_LEVEL, else LOGDEBUG.  If level is omitted, we assume 10.
def log(txt, level=10):
    if level > max(MAX_DEBUG_LOG_LEVEL, MAX_INFO_LOG_LEVEL):
        return
    if isinstance(txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addon_id__, txt)
    log_level = (xbmc.LOGERROR if level <= 0 else (xbmc.LOGNOTICE if level <= MAX_INFO_LOG_LEVEL else xbmc.LOGDEBUG))
    xbmc.log(msg=message.encode("utf-8"), level=log_level)

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

########################
#      News Class
########################
class News(object):

    def __init__(self, url=None):
        self.url    = url
        self.html   = _html(url)
    
    def _title(self):
        return self.html.find('h1').string.strip(' ').replace(u'\u2013', '-')
    
    def _title2(self):
        return self.html.find('h2').string.strip(' ').replace(u'\u2013', '-')
    
    def _thumb(self):
        div = self.html.find('div', {'class': 'pos_not_img_det'}) 
        return _full_url(div.img['src']).strip(' ')

    def _text(self):
        #return self.html.find('div', {'class': 'not_desc'}).string
        return 'path'

    def _date(self):
        return self.html.find('p', {'class': 'txt_10 not_date'}).string.strip(' ').replace(u'\u2013', '-')

########################
#    Category Class
########################
class Category(object):

    def __init__(self, name=None, media_type=None, url=None):
        self.name       = name
        self.media_type = media_type
        self.url        = url
        self.cat_id     = get_cat_id(self.url, 'category')

    def _name(self):
        return self.name.strip(' ').replace(u'\u2013', '-')

    def _cat_id(self):
        return self.cat_id.strip(' ')

    def _media_type(self):
        return self.media_type.strip(' ')
    
    def _thumb(self):
        """
        // TODO
        """
        return ''

    def _albums(self):
        return plugin.url_for('show_category_albums', 
                              media_type  = self.media_type, 
                              category_id = self.cat_id,
                              page     = 1) 

########################
#     Album Class
########################
class Album(object):

    def __init__(self, name=None, media_type=None, url=None, thumb=None, date=None):
        self.name       = name
        self.media_type = media_type
        self.url        = url
        self.thumb      = thumb
        self.date       = date
        self.album_id   = get_cat_id(self.url, 'album')

    def _name(self):
        return self.name.strip(' ').replace(u'\u2013', '-')

    def _album_id(self):
        return self.album_id.strip(' ')

    def _media_type(self):
        return self.media_type.strip(' ')
    
    def _thumb(self):
        return self.thumb.strip(' ')

    def _date(self):
        return convert_date(self.date, '%d-%m-%Y %H:%M', '%Y-%m-%d').replace(u'\u2013', '-')

    def _media(self):
        if   self.media_type == 'videos': return plugin.url_for('show_album_videos', album_id = self.album_id)
        elif self.media_type == 'photos': return plugin.url_for('play_slideshow', album_id = self.album_id) 

###########################
#   Navigation Menus
###########################
# |_ HEADLINES
# |_ NEWS
# |_ VIDEOS
# |_ PHOTOS
# |_ STADIUM
# |_ TICKETS
###########################

@plugin.route('/')
def show_menu():
    ##########################################################
    # menu     = { 'headlines'  : plugin.get_string(30001),
    #              'news'       : plugin.get_string(30002),
    #              'videos'     : plugin.get_string(30003),
    #              'photos'     : plugin.get_string(30004),
    #              'stadium     : plugin.get_string(30005),
    #              'tickets'    : plugin.get_string(30006),
    #              'calendar'   : plugin.get_string(30007),
    #            }
    ##########################################################

    items = [
        {'label': plugin.get_string(30001), 'path': plugin.url_for('show_headlines')},
        {'label': plugin.get_string(30002), 'path': plugin.url_for('show_news')},
        {'label': plugin.get_string(30003), 'path': plugin.url_for('show_media_categories', media_type = 'videos')},
        {'label': plugin.get_string(30004), 'path': plugin.url_for('show_media_categories', media_type = 'photos')},
        {'label': plugin.get_string(30005), 'path': plugin.url_for('show_stadium')},
        {'label': plugin.get_string(30006), 'path': plugin.url_for('show_tickets')},
        {'label': plugin.get_string(30007), 'path': plugin.url_for('show_calendar', date=datetime.now().strftime("%d-%m-%Y"))},
    ]

    return items

#######################
#   Navigation Routes
#######################

@plugin.route('/headlines/')
def show_headlines():

    html = _html(HOME_URL)

    uls = html.findAll('ul', {'class': 'dest_carr_list'})
    lis = [ul.findAll('li') for ul in uls]
    
    headlines = set()
    
    for li in chain(*lis):
        _news = News(li.a['href'])
        headlines.add((_news._title(),
                       _news._thumb(),
                       _news._text(),
                       _news._title2(),
                       _news._date()))

    items = [
        #{'label': str(label) + ' (' + str(date) + ')',
        {'label': label,
         'path': '',
         'thumbnail': thumbnail,
         'info': {'date': date,
                  'plot': text,
                  'plotoutline': text2,
                 },
        } for label, thumbnail, text, text2, date in headlines]    

    return sorted(items, key=lambda item: item['info']['date'], reverse=True)

@plugin.route('/news/')
def show_news():
    print ""

@plugin.route('/<media_type>/')
def show_media_categories(media_type):
    
    if   media_type == 'videos': html = _html(VIDEOS_URL)
    elif media_type == 'photos': html = _html(PHOTOS_URL)

    uls = html.findAll('ul', {'class': 'cat_list'})
    lis = [ul.findAll('li') for ul in uls]
    
    categories = set()
    
    for li in chain(*lis):
        _category = Category(name=li.a.string, media_type=media_type, url=li.a['href'])
        categories.add((_category._name(),
                        _category._albums()))

    items = [
        {'label': label,
         'path': path,
        } for label, path in categories]

    return sorted(items, key=lambda item: item['label'])

@plugin.route('/<media_type>/category/<category_id>/page/<page>')
def show_category_albums(media_type, category_id, page=1):
    
    page = int(page)
    
    if media_type == 'videos':
        category_url = VIDEOS_CATEGORY_URL.format(cat_id = category_id,
                                                  page   = page,
                                                  lang   = LANG) 
    elif media_type == 'photos':
        category_url = PHOTOS_CATEGORY_URL.format(cat_id = category_id,
                                                  page   = page,
                                                  lang   = LANG) 
    html = _html(category_url)
    uls = html.findAll('ul', {'class': 'pos_biglist_list'})
    lis = [ul.findAll('li') for ul in uls]
    
    albums = set()

    # find <previous page> | <next page> entries. add them if present
    (prev_page, next_page) = find_previous_next_page(page_html=html)
    
    for li in chain(*lis):
        _album = Album(name       = li.find('p', {'class': 'txt_11_dark'}).string, 
                       media_type = media_type, 
                       url        = li.a['href'],
                       thumb      = li.a.img['src'],
                       date       = li.find('p', {'class': 'txt_10'}).string)

        albums.add((_album._name(),
                    _album._media(),
                    _album._thumb(),
                    _album._date()))

    items = [
        #{'label': str(label) + ' (' + str(convert_date(date, '%Y-%m-%d', '%d-%m-%Y')) + ')',
        {'label': label,
         'path': path,
         'thumbnail': thumbnail,
         'info': {'date': date},
        } for label, path, thumbnail, date in albums]
    
    sorted_items = []
    for d in items:
        if d['label'] not in (s['label'] for s in sorted_items):
            sorted_items.append(d)

    sorted_items = sorted(sorted_items, key=lambda item: item['info']['date'], reverse=True) # sort by date descending

    if next_page:
        sorted_items.insert(int(len(sorted_items) + 1), {'label': plugin.get_string(30201),
                            'path': plugin.url_for('show_category_albums', media_type=media_type, category_id=category_id, 
                            page=str(page + 1)),})
    if page > 1:
        sorted_items.insert(0, {'label': plugin.get_string(30200),
                            'path': plugin.url_for('show_category_albums', media_type=media_type, 
                            category_id=category_id, page=str(page - 1)),})

    return plugin.finish(sorted_items, update_listing=True)

@plugin.route('/videos/album/<album_id>')
def show_album_videos(album_id):
    
    album_url = VIDEOS_ALBUM_URL.format(album_id = album_id, 
                                        lang     = LANG) 
    html = _html(album_url)
    uls  = html.findAll('ul', {'class': 'pos_biglist_vidlist'})
    lis  = [ul.findAll('li') for ul in uls]
    
    videos = set((li.find('p', {'class': 'txt_11'}).string, 
                  plugin.url_for('play_video', youtube_url=li.a['href']), 
                  li.a.img['src'])
             for li in chain(*lis))

    items = [
        {'label': label,
         'path': path,
         'is_playable': True,
         'thumbnail': thumbnail,
        } for label, path, thumbnail in videos]

    return sorted(items, key=lambda item: item['path'])

@plugin.route('/play_video/<youtube_url>')
def play_video(youtube_url):

    plugin_url = resolve_youtube_url(youtube_url)

    if plugin_url:
        return plugin.set_resolved_url(plugin_url)

@plugin.route('/play_slideshow/<album_id>')
def play_slideshow(album_id):
    
    album_url = PHOTOS_ALBUM_URL.format(album_id = album_id, 
                                        lang     = LANG)
    xbmc.log('Album url: ' + album_url)
    html = _html(album_url)
    uls  = html.findAll('ul', {'class': 'pos_biglist_imglist'})
    lis  = [ul.findAll('li') for ul in uls]
    
    images = []
    images = [
        {'path': str('http://www.slbenfica.pt' + li.a['href']).encode('utf-8'),
        } for li in chain(*lis)]
    
    #xbmc.log('Images to load: ' + str(images))
    start_slideshow(images)

@plugin.route('/stadium/')
def show_stadium():
    print ""

@plugin.route('/tickets/')    
def show_tickets():
    print ""

@plugin.route('/calendar/<date>/weeks/<weeks>')    
def show_calendar(date, numWeeks=1):
    
    _startdate = date(date[6:10], date[3:5], date[:2])
    calendar = Calendar(startDate=_startdate, numWeeks=numWeeks).get_calendar()


############################
#           MAIN
############################

#if __name__ == '__main__': 
#    plugin.run()
if ( __name__ == "__main__" ):
    xbmc.executebuiltin('Dialog.Close(all, true)')
    log( "############################################################", xbmc.LOGNOTICE )
    log( "#    %-50s    #" % __scriptname__, xbmc.LOGNOTICE )
    log( "#        default.py module                                 #", xbmc.LOGNOTICE )
    log( "#    %-50s    #" % __scriptID__, xbmc.LOGNOTICE )
    log( "#    %-50s    #" % __author__, xbmc.LOGNOTICE )
    log( "#    %-50s    #" % __version__, xbmc.LOGNOTICE )
    log( "############################################################", xbmc.LOGNOTICE )
    try:
        ui = gui.GUI( "script-cdartmanager.xml" , __addon__.getAddonInfo('path'), "Default")
        xbmc.sleep(2000)
        ui.doModal()
        del ui
    except:
        log( "Error in script occured", xbmc.LOGNOTICE )
        traceback.print_exc()
        dialog_msg( "close" )

############################