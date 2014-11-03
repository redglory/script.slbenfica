# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 redglory
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

import sys, re
from urlparse import urlparse, parse_qs, urljoin
from itertools import chain
import time
import urllib2
import codecs
from datetime import date, timedelta, datetime

import unicodedata

try:
    import json
except:
    import simplejson as json

# Beautiful Soup
from bs4 import BeautifulSoup as BS

# Common
from resources.lib.base import *

#-----------------------
#  Scrapping Methods
#-----------------------

def get_sport_id(sport):

    _sport = translate_sport(sport)

    return{
        'futebol'              : 12,
        'formacao'             : 38,
        'sl benfica b'         : 1914,
        'prospecao'            : 40,
        'futsal'               : 14,
        'hoquei'               : 16,
        'basquetebol'          : 17,
        'andebol'              : 18,
        'voleibol'             : 15,
        'xadrez'               : 2190,
        'automobilismo'        : 2781,
        'atletismo'            : 19,
        'artes marciais'       : 20,
        'bilhar'               : 21,
        'canoagem'             : 22,
        'desportos de combate' : 23,
        'ginastica'            : 24,
        'golfe'                : 25,
        'judo'                 : 26,
        'pesca desportiva'     : 28,
        'rugby'                : 29,
        'tenis de mesa'        : 31,
        'triatlo'              : 33,
        'paintball'            : 34,
        'natacao'              : 41,
        'clube'                : 44,
        'jogos olimpicos'      : 46,
        'outras'               : 45,
        'geral'                : 1614
    }[_sport]

def translate_sport(sport):
    return{
        'handball': 'andebol', 'balonmano': 'andebol',
        'football': 'futebol', 'futbol': 'futebol',
        'basketball': 'basquetebol', 'baloncesto': 'basquetebol',
        'funzone': 'funzone',
        'futsal': 'futsal',
        'hockey': 'hoquei',
        'rugby': 'rugby',
        'volleyball': 'voleibol',
        'table tennis': 'tenis de mesa',
        'athletics': 'atletismo', 
        'billiards': 'bilhar', 'billar': 'bilhar',
        'geral': 'geral',
        'automobilismo': 'automobilismo',
        'judo': 'judo',
    }[sport]

def get_sport_info(sport_id):

    # [id]: (sport_name, img)
    return{
            18    :('andebol', "Handball.png"),
            20    :('artes marciais', "Martial Arts.png"),
            19    :('atletismo', "Athletics.png"),
            2781  :('automobilismo', "Racing.png"),
            2132  :('bancada familia', "Racing.png"),
            17    :('basquetebol', "Basketball.png"),
            21    :('bilhar', "Billiard.png"),
            22    :('canoagem', "Canoe Racing.png"),              
            44    :('clube', "Club.png"),
            23    :('desportos de combate', "Boxing.png"),
            37    :('equipa principal', "Team.png"),
            39    :('escolas geracao benfica', "Team.png"),
            38    :('formacao', "Team.png"),
            4     :('funzone', "FunZone.png"),
            12    :('futebol', "Football.png"),               
            14    :('futsal', "Football.png"),                
            1614  :('geral', "Other.png"),                 
            24    :('ginastica', "Gymnastics.png"),
            25    :('golfe', "Golf.png"),        
            16    :('hoquei', "Hockey.png"),                
            1814  :('hoquei feminino', "Hockey.png"),                
            46    :('jogos olimpicos', "Olympic Games.png"),
            26    :('judo', "Judo.png"),                  
            41    :('natacao', "Swimming.png"),  
            45    :('outras', "Other.png"),
            34    :('paintball', "Paintball.png"),          
            28    :('pesca desportiva', "Sport Fishing.png"),
            40    :('prospecao', "Team.png"), 
            29    :('rugby', "Rugby.png"),      
            2030  :('rugby feminino', "Rugby.png"),
            1914  :('sl benfica b', "Club.png"),        
            31    :('tenis de mesa', "Table Tennis.png"),         
            33    :('triatlo',"Triatlo.png"),
            15    :('voleibol', "Volleyball.png"),              
            2190  :('xadrez', "Chess.png"),

    }[sport_id]


def get_cat_id(url, otype):

    pattern = '/cat/(.*?)/'

    match = re.search(pattern, url)
    
    return match.group(1)

def find_previous_next_page(page_html):

    prev_page = page_html.find('a', {'class': 'ic_arrow_prev'})
    next_page = page_html.find('a', {'class': 'ic_arrow_next'})
    
    prev_page_url = True if prev_page else False
    next_page_url = True if next_page else False

    return prev_page_url, next_page_url

#-----------------------
#  Scrapping class
#-----------------------
class SLB(object):
    #-----------------------
    #   Base URLs
    #-----------------------
    #   TYPES:
    #------------------------------------------
    #   {media_type} = videos | photos
    #   {lang}       = pt-pt  | es-es | en-us
    #------------------------------------------
    def __init__(self, lang='pt-PT'):
        
        self.LANG = lang
        self.ROOT_URL            = 'http://www.slbenfica.pt/'
        self.HOME_URL            = 'http://www.slbenfica.pt/{lang}/home.aspx'.format(lang=lang)
        self.NEWS_URL            = 'http://www.slbenfica.pt/{lang}/noticias.aspx'.format(lang=lang)
        self.VIDEOS_URL          = 'http://www.slbenfica.pt/{lang}/videos.aspx'.format(lang=lang)
        self.PHOTOS_URL          = 'http://www.slbenfica.pt/{lang}/fotos.aspx'.format(lang=lang)
        self.NEWS_CATEGORY_URL   = 'http://www.slbenfica.pt/noticias/listagemdenoticia/tabid/2790/cat/{album_id}/language/{lang}/Default.aspx'.format(lang=lang)
        self.VIDEOS_CATEGORY_URL = 'http://www.slbenfica.pt/videos/albuns/tabid/2805/LCmid/9435/filter-Page/{page}/cat/{cat_id}/filter-eType/all/filter-Tags/all/sort-Asc/default/sort-Desc/default/language/{lang}/Default.aspx'.format(lang=lang)
        self.PHOTOS_CATEGORY_URL = 'http://www.slbenfica.pt/fotos/albuns/tabid/2802/LCmid/9751/filter-Page/{page}/cat/{cat_id}/filter-eType/all/filter-Tags/all/sort-Asc/default/sort-Desc/default/language/{lang}/Default.aspx'.format(lang=lang)
        self.VIDEOS_ALBUM_URL    = 'http://www.slbenfica.pt/video/detalhealbum/tabid/2806/cat/{album_id}/language/{lang}/Default.aspx'.format(lang=lang)
        self.PHOTOS_ALBUM_URL    = 'http://www.slbenfica.pt/fotos/detalhealbum/tabid/2803/cat/{album_id}/language/{lang}/Default.aspx'.format(lang=lang)
        self.YOUTUBE_URL         = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid={id}'

    def get_news_by_category(self, cat_id):
        pass
    
    def get_videos_by_category(self, cat_id):
        pass

    def get_photos_by_category(self, cat_id):
        pass

    def get_sport_categories(self, cat_id):
        pass

    def get_sport_albums(self, cat_id):
        pass

    def get_headlines(self):

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

    def get_media_categories(self, media_type):
    
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

    def get_category_albums(self, media_type, category_id, page=1):
        
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
    
        return sorted_items

    def get_album_videos(self, album_id):
        
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

    def play_slideshow(self, album_id):
        
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

    def get_calendar(self, date, numWeeks=1):
        
        # needs re-working!!!
        _startdate = date(date[6:10], date[3:5], date[:2])
        calendar = Calendar.get_calendar(startDate=_startdate, numWeeks=numWeeks, lang=self.LANG)


#---------------------
#      News Class
#---------------------
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

#---------------------
#    Category Class
#---------------------
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

#---------------------
#     Album Class
#---------------------
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


#-----------------------
#  CALENDAR METHODS
#-----------------------
class Calendar(object):
    
    def __init__(self, startDate=date.today(), numWeeks='1', language='pt-PT'):

        self.startDate = startDate
        self.numWeeks = numWeeks
        self.language = language
        self.first_day, self.last_day = Calendar.first_last_day(self.startDate, self.numWeeks, self.language)

    @staticmethod
    def first_last_day(day, numWeeks=1, language='pt-pt'):

        if numWeeks:
            end_day = (7 * int(numWeeks)) - 1
        
        day_of_week = day.weekday()
    
        to_beginning_of_week = timedelta(days=day_of_week)
        beginning_of_week = day - to_beginning_of_week
    
        to_end_of_week = timedelta(days=end_day - day_of_week)
        end_of_week = day + to_end_of_week
        
        if language.lower() == 'pt-pt':
            return (beginning_of_week.strftime("%d-%m-%Y"), end_of_week.strftime("%d-%m-%Y"))
        elif language.lower() == 'en-us':
            return (beginning_of_week.strftime("%m/%d/%Y"), end_of_week.strftime("%m/%d/%Y"))
        elif language.lower() == 'es-es':
            return (beginning_of_week.strftime("%d/%m/%Y"), end_of_week.strftime("%d/%m/%Y"))

    @staticmethod
    def get_calendar(startDate=date.today(), numWeeks='1', language='pt-pt'):

        first_day, last_day = Calendar.first_last_day(startDate, numWeeks, language)

        url = 'http://m.slbenfica.pt/HttpHandlers/SLBSportsAgenda.ashx?ModID=1172&LvlId=-1&AgendaStartDate='+first_day+'%2000:00:00&NumWeeks='+numWeeks+'&CurrentType=Event&Culture='+language+'&Mobile=true&PurchaseTicketURL=https://m.slbenfica.pt/'+language+'/bilhetes/comprar.aspx'

        # convert html to json
        calendar = {}
        sports = []
        sports_events = {}
        events = []
        event  = {}

        html_soup = BS(download_page(url).read().decode('utf-8', 'ignore'))
        
        uls = html_soup.findAll('ul', {'class': 'agEvt'})
        lis = [ul.findAll('li') for ul in uls]

        for li in chain(*lis):
            
            # event date
            day = int(li.find('span', {'class': 't20wt'}).string)
            _month = li.find('p', {'class': 't9red'}).string
            month = monthToNum(_month)
            year = datetime.now().year
            if _month < datetime.now().month:
                year = year + 1
            _date = date(year, month, day).strftime("%d-%m-%Y")
            weekday                 = li.find('p', {'class': 't9lt'}).string

            # sport
            _sport                  = li.find('div', {'class': 'agMod t14red'}).string
            sportName               = remove_accents(_sport) # no accents

            # sport event
            event["date"]           = _date
            event["event"]          = li.find('p', {'class': 'agTit t12wtB'}).string
            event["local"]          = li.find('p', {'class': 'agLoc t12lt2B'}).string
            event["description"]    = li.find('span', {'class': 't12lt'}).string if li.find('span', {'class': 't12lt'}) else ""
            img_home                = li.find('div', {'class': 'eHo'})
            event["home_team_img"]  = _full_url(img_home.img['src']) if img_home else ""
            event["home_team_name"] = img_home.img['alt'] if img_home else ""
            img_away                = li.find('div', {'class': 'eVi'})
            event["away_team_img"]  = _full_url(img_away.img['src']) if img_away else ""
            event["away_team_name"] = img_away.img['alt'] if img_away else ""
            event["buy_ticket"]     = li.find('a', {'class': 'agBt btDark'}).href if li.find('a', {'class': 'agBt btDark'}) else ""

            # build sports events
            if sports_events.get(sportName): # sport already exists
                sports_events[sportName].append(event)
            else: # new sport -> add to dict with event
                events.append(event)
                sports_events[sportName] = events
        
            event = {}
            events = []

        #---------------------------------------------------------------------------------------
        #     build json format
        #---------------------------------------------------------------------------------------
        # structure:
        # { "calendar": { "type": "list"
        #                 "sports": [ {"id": "5", "name": "futebol", "events": [...] }
        #                             {"id": "2", "name": "automobilismo", "events": [...] }
        #                             {"id": "6", "name": "futsal", "events": [...] }
        #                           ]
        #                 "start_date" : "01-01-2014"
        #                 "end_date"   : "15-03-2014"
        # }
        #---------------------------------------------------------------------------------------

        calendar["calendar"] = {"type": "list", "start_date" : first_day, "end_date": last_day}

        for k, v in sports_events.iteritems():
            _id, _img = get_sport_info(k)
            sports.append({"id": _id, "name": k, "img": _img, "events": v})

        calendar["calendar"]["sports"] = sports

        return calendar if calendar else []