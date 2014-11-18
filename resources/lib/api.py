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
from urlparse import urlparse, parse_qs, urljoin, urlsplit, urlunsplit
from itertools import chain
import time
from urllib import quote, unquote
import urllib2
import codecs
from datetime import date, timedelta, datetime
import unicodedata

try:
    import json
except:
    import simplejson as json

from bs4 import BeautifulSoup, NavigableString, Tag

# Common
from resources.lib.base import _html, _full_url, lw, Addon, Controls, Mode, kodi_text, stringify_text, set_coloring, set_carriage_return, set_bold, set_italic, clean_color, kodi_color, replace_br, replace_nbsp, replace_nl

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
    def __init__(self, lang='pt-PT', kodi=False):
        
        self.LANG                = lang
        self.ROOT_URL            = 'http://www.slbenfica.pt/'
        self.HOME_URL            = 'http://www.slbenfica.pt/{lang}/home.aspx'.format(lang=lang)
        self.NEWS_URL            = 'http://www.slbenfica.pt/{lang}/noticias.aspx'.format(lang=lang)
        self.VIDEOS_URL          = 'http://www.slbenfica.pt/{lang}/videos.aspx'.format(lang=lang)
        self.PHOTOS_URL          = 'http://www.slbenfica.pt/{lang}/fotos.aspx'.format(lang=lang)
        self.NEWS_CATEGORY_URL   = 'http://www.slbenfica.pt/noticias/listagemdenoticia/tabid/2790/cat/{album_id}/language/{lang}/Default.aspx'
        self.VIDEOS_CATEGORY_URL = 'http://www.slbenfica.pt/videos/albuns/tabid/2805/LCmid/9435/filter-Page/{page}/cat/{cat_id}/filter-eType/all/filter-Tags/all/sort-Asc/default/sort-Desc/default/language/{lang}/Default.aspx'
        self.PHOTOS_CATEGORY_URL = 'http://www.slbenfica.pt/fotos/albuns/tabid/2802/LCmid/9751/filter-Page/{page}/cat/{cat_id}/filter-eType/all/filter-Tags/all/sort-Asc/default/sort-Desc/default/language/{lang}/Default.aspx'
        self.VIDEOS_ALBUM_URL    = 'http://www.slbenfica.pt/video/detalhealbum/tabid/2806/cat/{album_id}/language/{lang}/Default.aspx'
        self.PHOTOS_ALBUM_URL    = 'http://www.slbenfica.pt/fotos/detalhealbum/tabid/2803/cat/{album_id}/language/{lang}/Default.aspx'
        self.YOUTUBE_URL         = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid={id}'

        self.KODI = kodi

    def get_sport_id(self, sport):
    
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
            'funzone'              : 1707,
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
    
    def translate_sport(self, sport):
        try:
            return{
                'athletics'           : 'atletismo', 
                'baloncesto'          : 'basquetebol',
                'balonmano'           : 'andebol',
                'basketball'          : 'basquetebol', 
                'billar'              : 'bilhar',
                'billiards'           : 'bilhar',
                'canoeing'            : 'canoagem',
                'club'                : 'clube',
                'combat sports'       : 'desportos de combate',
                'deportes de combate' : 'desportos de combate',
                'handball'            : 'andebol', 
                'hockey'              : 'hoquei',
                'football'            : 'futebol',
                'formation'           : 'formacao',
                'futbol'              : 'futebol', 
                'gimnasia'            : 'ginastica',
                'gymnastics'          : 'ginastica',
                'golf'                : 'golfe',
                'juegos olimpicos'    : 'jogos olimpicos',
                'martial arts'        : 'artes marciais',
                'natacion'            : 'natacao',
                'olimpic games'       : 'jogos olimpicos',
                'others'              : 'outras',
                'outro'               : 'outras',
                'piraguismo'          : 'canoagem',
                'prospeccion'         : 'prospecao',
                'prospecting'         : 'prospecao',
                'sport fishing'       : 'pesca desportiva',
                'swimming'            : 'natacao',
                'table tennis'        : 'tenis de mesa',
                'triathlon'           : 'triatlo',
                'triatlon'            : 'triatlo',
                'volleyball'          : 'voleibol',
                'youth teams'         : 'formacao' 
            }[sport]
        except: # are the same
            return sport
    
    def get_sport_info(self, sport_id):
    
        # [id]: (sport_name, img)
        return{
                18    :(Addon.__translate__(31000), "Handball.png"),
                20    :(Addon.__translate__(31001), "Martial Arts.png"),
                19    :(Addon.__translate__(31002), "Athletics.png"),
                2781  :(Addon.__translate__(31003), "Racing.png"),
                2132  :(Addon.__translate__(31004), "Club.png"),
                17    :(Addon.__translate__(31005), "Basketball.png"),
                21    :(Addon.__translate__(31006), "Billiard.png"),
                22    :(Addon.__translate__(31007), "Canoeing.png"),              
                44    :(Addon.__translate__(31008), "Club.png"),
                23    :(Addon.__translate__(31009), "Boxing.png"),
                37    :(Addon.__translate__(31010), "Team.png"),
                39    :(Addon.__translate__(31011), "Team.png"),
                38    :(Addon.__translate__(31012), "Team.png"),
                1707  :(Addon.__translate__(31013), "FunZone.png"),
                12    :(Addon.__translate__(31014), "Football.png"),               
                14    :(Addon.__translate__(31015), "Football.png"),                
                1614  :(Addon.__translate__(31016), "Other.png"),                 
                24    :(Addon.__translate__(31017), "Gymnastics.png"),
                25    :(Addon.__translate__(31018), "Golf.png"),        
                16    :(Addon.__translate__(31019), "Hockey.png"),                
                1814  :(Addon.__translate__(31020), "Hockey.png"),                
                46    :(Addon.__translate__(31021), "Olympic Games.png"),
                26    :(Addon.__translate__(31022), "Judo.png"),                  
                41    :(Addon.__translate__(31023), "Swimming.png"),  
                45    :(Addon.__translate__(31024), "Other.png"),
                34    :(Addon.__translate__(31025), "Paintball.png"),          
                28    :(Addon.__translate__(31026), "Sport Fishing.png"),
                40    :(Addon.__translate__(31027), "Team.png"), 
                29    :(Addon.__translate__(31028), "Rugby.png"),      
                2030  :(Addon.__translate__(31029), "Rugby.png"),
                1914  :(Addon.__translate__(31030), "Club.png"),        
                31    :(Addon.__translate__(31031), "Table Tennis.png"),         
                33    :(Addon.__translate__(31032), "Triathlon.png"),
                15    :(Addon.__translate__(31033), "Volleyball.png"),              
                2190  :(Addon.__translate__(31034), "Chess.png")
        }[sport_id]
    
    
    def get_cat_id(self, url, otype):
    
        pattern = '/cat/(.*?)/'
        match = re.search(pattern, url)

        return match.group(1)
    
    def find_previous_next_page(self, page_html):
    
        prev_page = page_html.find('a', class_='ic_arrow_prev')
        next_page = page_html.find('a', class_='ic_arrow_next')
        
        prev_page_url = True if prev_page else False
        next_page_url = True if next_page else False
    
        return prev_page_url, next_page_url

    def get_next_matches(self):
        #---------------------------------------------------------------------------------------
        #     Next Matches (json format)
        #---------------------------------------------------------------------------------------
        #                                       structure:
        #---------------------------------------------------------------------------------------
        # [{"id"    : "12", 
        #    "sport" : "futebol",
        #    "match_info" : {"competition"  : "10ª Jornada - Primeira Liga"
        #                    "match"        : "Nacional da Madeira vs. SL Benfica"
        #                    "date"         : "Domingo, 09-11-2014 16:00"
        #                    "local"        : "Estádio da Madeira"}
        #   },
        #   {"id"    : "14", 
        #    "sport" : "futsal", 
        #    "match_info" : {"competition"  : "9ª Jornada - Campeonato Nacional"
        #                    "match"        : "Belenenses vs. SL Benfica"
        #                    "date"         : "Domingo, 09-11-2014 17:00"
        #                    "local"        : "Pavilhão Acácio Rosa"},
        #   },
        # ]
        #---------------------------------------------------------------------------------------

        COMPETITION = 'dnn_ctr8809_SLBSportsAgendaWidget_RepeaterGames_RepeaterGamesByMainSport_{index}_AgendaWidgetEvent_0_CompetitionNameLit_0'
        MATCH       = 'dnn_ctr8809_SLBSportsAgendaWidget_RepeaterGames_RepeaterGamesByMainSport_{index}_AgendaWidgetEvent_0_LabelGameDesc_0'
        MATCH_DATE  = 'dnn_ctr8809_SLBSportsAgendaWidget_RepeaterGames_RepeaterGamesByMainSport_{index}_AgendaWidgetEvent_0_LabelGameDateDesc_0'
        MATCH_LOCAL = 'dnn_ctr8809_SLBSportsAgendaWidget_RepeaterGames_RepeaterGamesByMainSport_{index}_AgendaWidgetEvent_0_LabelGameLocalDesc_0'
    
        html = _html(self.HOME_URL)
        
        # Sports id's list
        sports_lis  = html.find('ul', class_='next_games_categories_menu clearfix').find_all('li')
    
        # Sports next matches
        matches_uls = html.find_all('ul', class_='next_games_competitions')
        matches_lis = [match_ul.find_all('li')[0] for match_ul in matches_uls]
    
        matches = []
        for index, match_li in enumerate(matches_lis):
            
            competition = match_li.find('span', {'id': COMPETITION.format(index=str(index))}).string
            match       = match_li.find('span', {'id': MATCH.format(index=str(index))}).string
            if match.find('vs.') != -1:
                home_team, away_team = match.split('vs.')
            match_date  = match_li.find('span', {'id': MATCH_DATE.format(index=str(index))}).string
            match_local = match_li.find('span', {'id': MATCH_LOCAL.format(index=str(index))}).string
            matches.append({'competition': competition.strip(' ...'), 
                            'home_team': home_team.strip(' '), 
                            'away_team': away_team.strip(' '), 
                            'match_date': match_date, 
                            'match_local': match_local.strip(' ...').strip(' -')})    
    
        next_matches = []
        for index, sport_li in enumerate(sports_lis):
            _id = int(sport_li.find('a')['id'])
            if _id != 1707: # remove funzone events
                _sport, _thumb = self.get_sport_info(_id)
                next_matches.append({'id': _id,
                                     'sport': _sport,
                                     'thumbnail': _thumb,
                                     'match_info': {'competition_name' : matches[index]['competition'],
                                                    'competition_home_team': matches[index]['home_team'],
                                                    'competition_away_team': matches[index]['away_team'],
                                                    'competition_date' : matches[index]['match_date'],
                                                    'competition_local': matches[index]['match_local']}
                                })
        return next_matches

    #---------------------
    #    CLUB METHODS
    #---------------------    
    def get_club_structure(self):

        html = _html('http://www.slbenfica.pt/{lang}/clube/org%C3%A3ossociais.aspx'.format(lang=self.LANG))
    
        club_structure = {}
        
        table = html.find('table', {'class': 'pos_tab_generic'}) 
        # table headers
        header = table.find('tr', {'class': 'tab_top_red'})
        titles = ['board', 'assembly', 'fiscal']
    
        header.extract() # remove header row from table
    
        members = [tr.find_all('td') for tr in table.find_all('tr')]
    
        for idx, title in enumerate(titles): # for each table column
            club_structure[title] = [{'position': member[idx].find('p', {'class': 'txt_11_red'}).string if member[idx].find('p', {'class': 'txt_11_red'}) else '',
                                      'name': member[idx].find('p', {'class': 'txt_11_dark'}).string if member[idx].find('p', {'class': 'txt_11_dark'}) else '',
                                      'affiliate': member[idx].find('p', {'class': 'txt_10'}).string if member[idx].find('p', {'class': 'txt_10'}) else ''}
                                      for member in members]

        return club_structure

    def get_club_foundation_history(self):
        # foundation
        html = _html('http://www.slbenfica.pt/{lang}/slb/historia/fundacao.aspx'.format(lang=self.LANG))
        text = html.find('div', id='dnn_ctr664_MLHTML_lblContent')
        h1 = text.find('h1')
        h1.extract() # remove title
        if self.KODI:
            return {'title': h1.string,
                    'img': _full_url(self.ROOT_URL, html.find('div', class_='main_cont2_bannertop').img['src']),
                    'text': kodi_text(text)}
        else:
            return {'title': h1.string,
                    'img': _full_url(self.ROOT_URL, html.find('div', class_='main_cont2_bannertop').img['src']),
                    'text': stringify_text(text)}            


    def get_club_symbols_history(self):
        # symbols
        html = _html('http://www.slbenfica.pt/{lang}/slb/historia/simbolos.aspx'.format(lang=self.LANG))
        symbols = html.find('ul', class_='main_cont2_list')
        symbols.extract() # remove list of symbols to get text only
        intro = html.find('div', id='dnn_ctr670_MLHTML_lblContent')
        title1 = intro.find('h1')
        title1.extract()
        title2 = intro.find('h2')
        title2.extract()
        title = ' - '.join([title1.string.encode('utf-8'), title2.string.encode('utf-8')]).decode('utf-8')
        
        if self.KODI:
            return {'title': title, 
                    'text': kodi_text(intro),
                    'symbols': [{'img': _full_url(self.ROOT_URL, symbol.find('div', class_='main_cont2_list_img').img['src']),
                                 'text': kodi_text(symbol.find('div', class_='main_cont2_list_det'))} 
                               for symbol in symbols.find_all('li')]}
        else:
            return {'title': title, 
                    'text': stringify_text(intro),
                    'symbols': [{'img': _full_url(self.ROOT_URL, symbol.find('div', class_='main_cont2_list_img').img['src']),
                                 'text': stringify_text(symbol.find('div', class_='main_cont2_list_det'))} 
                               for symbol in symbols.find_all('li')]}                               

    def get_club_presidents_history(self):
        # presidents
        html = _html('http://www.slbenfica.pt/{lang}/slb/historia/presidentes.aspx'.format(lang=self.LANG))
    
        intro = html.find('div', id='dnn_ctr2916_MLHTML_lblContent')
        title = intro.find('h1') # title
        title.extract()
        tags = ['div', 'a']
        for tag in tags:
            block = intro.find(tag) # remove tags from intro
            block.extract()
    
        def get_president_info(president):
            link = president.find('p', class_='view_more').a['href']
            view_more = _html(link.encode('utf-8'))
            if view_more.find('h2'): 
                info = view_more.find('h2').parent
                a = info.find('a')
                a.extract()
            if self.KODI:
                short = kodi_text(president.find('p', class_='description'))
                text = kodi_text(info)
            else:
                short = stringify_text(president.find('p', class_='description'))
                text = stringify_text(info)
            return {'short': short, 'long': text}
    
        if self.KODI:
            return {'title': title.get_text(strip=True),
                    'text': kodi_text(intro),
                    'list': [{'num': index + 1,
                              'thumb': re.search(r"(.*?)\?.*?", _full_url(self.ROOT_URL, html.find('a', id='dnn_ctr2917_Presidentes_presidentRepeater_presidentLink_{index}'.format(index=index)).img['src'])).group(1),
                              'period': president.find('p', class_='line_1st').string,
                              'name': president.find('p', class_='line_2nd').string,
                              'description': get_president_info(president)}
                            for index, president in enumerate(html.find('div', class_='modal_window_content clearfix').find_all('div', class_='body'))]}
        else:
            return {'title': title.get_text(strip=True),
                    'text': stringify_text(intro),
                    'list': [{'num': index + 1,
                              'thumb': re.search(r"(.*?)\?.*?", _full_url(self.ROOT_URL, html.find('a', id='dnn_ctr2917_Presidentes_presidentRepeater_presidentLink_{index}'.format(index=index)).img['src'])).group(1),
                              'period': president.find('p', class_='line_1st').string,
                              'name': president.find('p', class_='line_2nd').string,
                              'description': get_president_info(president)}
                            for index, president in enumerate(html.find('div', class_='modal_window_content clearfix').find_all('div', class_='body'))]}

    def get_club_honours_history(self):
        # honours
        html = _html('http://www.slbenfica.pt/{lang}/slb/historia/condecoracoes.aspx'.format(lang=self.LANG))
        ul = html.find('ul', class_="pos_ul_generic")
        honours = []
        for h3 in ul.find_all('h3'):
            for tag in h3.next_siblings:
                if tag.name == 'p':
                    if self.KODI:
                        honour = {'name': h3.string, 'awards': kodi_text(tag)}
                    else:
                        honour = {'name': h3.string, 'awards': stringify_text(tag)}
                    honours.append(honour)
                    continue
                if tag.name == 'h3':
                    break
        return {'title': ul.parent.find('h1').string,
                'img': _full_url(self.ROOT_URL, html.find('div', class_='main_cont2_bannertop').img['src']),
                'honours': honours}

    def get_club_decades_history(self):
        html = _html('http://www.slbenfica.pt/{lang}/slb/historia/decadaadecada.aspx'.format(lang=self.LANG))
        
        def get_decade_info(decade):
            link = decade.find('div', class_='main_cont2_list_img').a['href']
            info = _html(link.encode('utf-8')).find('div', class_=re.compile('spc_pt17')).find('p').parent
            if self.KODI:
                return kodi_text(info)
            else:
                return stringify_text(info)

        decades = html.find('ul', class_='main_cont2_list').find_all('li')
        return {'decades': [{'decade': decade.find('div', class_='main_cont2_list_det').find('p', class_='txt_list_title').string.encode('utf-8'),
                             'img': _full_url(self.ROOT_URL, decade.find('div', class_='main_cont2_list_img').a.img['src']),
                             'text': get_decade_info(decade)}
                           for decade in decades]}

    def get_club_top_players_history(self):
        
        def get_top_players_position_info(top_players_position):
            link = top_players_position.find('div', class_='main_cont2_list_img').a['href']
            original = _html('http://www.slbenfica.pt/pt-pt/slb/historia/grandesjogadores/defesasdireitos.aspx'.encode('utf-8')).find('div', class_=re.compile('spc_pt17')).find('p').parent
            info = original
            # remove title
            title = info.h1
            title.extract()
            if self.KODI:
                # replace </br> with [CR]
                replace_br(info)
                # replace &nbsp; with [CR]
                replace_nbsp(info)
                # first extract all images from players
            players_images = []
            for img in info.find_all('img'):
                players_images.append(_full_url(self.ROOT_URL, img['src'].encode('utf-8')))
                img.extract()
            # now, process only <p> tags. Every <p class="txt_12_dark"> is a new player
            top_players = []
            players_names = []
            players_texts = []
            player_text = []

            first = True
            for tag in info.descendants:
                if isinstance(tag, Tag):
                    if tag.name == 'p': 
                        if unicode('txt_12_dark') in [values for values in chain(*tag.attrs.values())]: # found first/next player name
                            if first: # first player, just append to players names table
                                players_names.append(tag.string.strip(' '))
                                first = False
                            else: # process previous player text
                                players_names.append(tag.string.strip(' ')) # add new player name
                                if self.KODI:
                                    players_texts.append(kodi_text(player_text))
                                else:
                                    players_texts.append(stringify_text(player_text))
                                player_text = [] # refresh
                        else: # text from same player
                            player_text.append(tag.string.strip(' '))
                else: continue
            # process last player text...
            if self.KODI:
                players_texts.append(kodi_text(player_text))
            else:
                players_texts.append(stringify_text(player_text))

            return [{'player': players_names[index],
                     'img': players_images[index],
                     'text': players_texts[index]}
                   for index in range(len(players_names))]
            
        html = _html('http://www.slbenfica.pt/{lang}/slb/historia/grandesjogadores.aspx'.format(lang=self.LANG))
        top_players_positions = html.find('ul', class_='main_cont2_list').find_all('li')
        return {'top_players_history': [{'top_players_position': top_players_position.find('div', class_='main_cont2_list_det').find('p', class_='txt_list_title').string.encode('utf-8'),
                                         'short': top_players_position.find('div', class_='main_cont2_list_det').find('p', class_='txt_list_desc').string.encode('utf-8'),  
                                         'img': _full_url(self.ROOT_URL, top_players_position.find('div', class_='main_cont2_list_img').a.img['src']),
                                         'top_players': get_top_players_position_info(top_players_position)}
                                       for top_players_position in top_players_positions]}


    def get_club_founder_history(self):
        html = _html('http://www.slbenfica.pt/{lang}/slb/historia/cosmedamiao.aspx'.format(lang=self.LANG))
    
        founder = html.find('div', id='dnn_ctr4148_MLHTML_lblContent')
        title = founder.find('h1')
        title.extract()
        author = founder.find('p', class_='txt_10')
        author.extract()
        
        if self.KODI:
            return {'title': title.string.strip(' '),
                    'text': kodi_text(founder)}
        else:
            return {'title': title.string.strip(' '),
                    'text': stringify_text(founder)}

    def get_club_history(self):

        # fundation history
        foundation_history = get_club_foundation_history()
        # symbols history
        symbols_history = get_club_symbols_history()
        # presidents history
        presidents_history = get_club_presidents_history()
        # honours and decorations history
        honours_history = get_club_honours_history()
 
        club_history = {'foundation': foundation_history,
                        'symbols': symbols_history,
                        'presidents': presidents_history,
                        'honours': honours_history}
            
        return club_history

    #---------------------
    #    NEWS METHODS
    #---------------------
    def get_news_info(self, link):
        news = _html(link.encode('utf-8'))
        if self.KODI:
            return {'title': news.find('h1').string.strip(' '),
                    'title2': news.find('h2').string.strip(' '),
                    'text': kodi_text(news.find('div', class_='not_desc')),
                    'thumb': re.search(r"(.*?)\?.*?", _full_url(self.ROOT_URL, news.find('div', class_='pos_not_img_det').img['src'])).group(1),
                    'date': news.find('p', class_='txt_10 not_date').string.strip(' ')}
        else:
            return {'title': news.find('h1').string.strip(' '),
                    'title2': news.find('h2').string.strip(' '),
                    'text': stringify_text(news.find('div', class_='not_desc')),
                    'thumb': re.search(r"(.*?)\?.*?", _full_url(self.ROOT_URL, news.find('div', class_='pos_not_img_det').img['src'])).group(1),
                    'date': news.find('p', class_='txt_10 not_date').string.strip(' ')}

    def get_headlines(self):

        html = _html(self.HOME_URL)
    
        uls = html.find_all('ul', class_='dest_carr_list')
        lis = [ul.find_all('li') for ul in uls]

        return {'headlines': [get_news_info(li.a['href']) for li in chain(*lis)]}


    #---------------------------------
    #    VIDEOS AND PHOTOS METHODS
    #---------------------------------
    def get_category_info(self, media_type, link):
        category = _html(link.encode('utf-8'))

        cat_id     = get_cat_id(link, 'category')
        sport_info = get_sport_info(int(cat_id))

        return {'name': sport_info[0].encode('utf-8'),
                'thumb': os.path.join(Addon.__imagespath__ + sport_info[1]).encode('utf-8'),
                'albums': get_category_albums(media_type, cat_id)}

    def get_media_categories(self, media_type):
    
        if   media_type == 'videos': html = _html(self.VIDEOS_URL)
        elif media_type == 'photos': html = _html(self.PHOTOS_URL)
    
        uls = html.find_all('ul', class_='cat_list')
        lis = [ul.find_all('li') for ul in uls]
        
        categories = [get_category_info(media_type, li.a['href']) for li in chain(*lis)]
        
        return {'categories': categories}

    def get_category_albums(self, media_type, category_id, page=1):
        
        page = int(page)
        
        if media_type == 'videos':
            category_url = self.VIDEOS_CATEGORY_URL.format(cat_id = category_id,
                                                           page   = page,
                                                           lang   = self.LANG) 
        elif media_type == 'photos':
            category_url = self.PHOTOS_CATEGORY_URL.format(cat_id = category_id,
                                                           page   = page,
                                                           lang   = self.LANG) 
        html = _html(category_url)
        uls = html.find_all('ul', class_='pos_biglist_list')
        lis = [ul.find_all('li') for ul in uls]
        
        albums = set()
    
        # find <previous page> | <next page> entries. add them if present
        (prev_page, next_page) = find_previous_next_page(page_html=html)
        
        for li in chain(*lis):
            _album = Album(name       = li.find('p', class_='txt_11_dark').string, 
                           media_type = media_type, 
                           url        = li.a['href'],
                           thumb      = li.a.img['src'],
                           date       = li.find('p', class_='txt_10').string)
    
            albums.add((_album._name(),
                        _album._media(),
                        _album._thumb(),
                        _album._date()))
    
        items = [
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
            sorted_items.insert(int(len(sorted_items) + 1), 
                                {'label': Addon.__translate__(30201),
                                 'path': get_category_albums(media_type  = media_type, 
                                                             category_id = category_id, 
                                                             page        = str(page + 1)),
                                })
        if page > 1:
            sorted_items.insert(0, 
                                {'label': Addon.__translate__(30200),
                                  'path': get_category_albums(media_type  = media_type, 
                                                              category_id = category_id, 
                                                              page        = str(page - 1)),
                                })
    
        return sorted_items

    def get_album_videos(self, album_id):
        
        video_album_url = self.VIDEOS_ALBUM_URL.format(album_id = album_id, 
                                                       lang     = self.LANG) 
        html = _html(video_album_url)
        uls  = html.find_all('ul', class_='pos_biglist_vidlist')
        lis  = [ul.find_all('li') for ul in uls]
        
        videos = set((li.find('p', class_='txt_11').string, 
                      play_video(youtube_url=li.a['href']), 
                      li.a.img['src'])
                 for li in chain(*lis))
    
        items = [
            {'label': label,
             'path': path,
             'is_playable': True,
             'thumbnail': thumbnail,
            } for label, path, thumbnail in videos]
    
        return sorted(items, key=lambda item: item['label'])

    def get_album_photos(self, album_id):
        
        photo_album_url = self.PHOTOS_ALBUM_URL.format(album_id = album_id, 
                                                       lang     = self.LANG)
        html = _html(photo_album_url)
        uls  = html.find_all('ul', class_='pos_biglist_imglist')
        lis  = [ul.find_all('li') for ul in uls]
        
        images = []
        images = [
            {'path': str('http://www.slbenfica.pt' + li.a['href']).encode('utf-8'),
            } for li in chain(*lis)]

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
            if   self.media_type == 'videos': return get_album_videos(album_id = self.album_id)
            elif self.media_type == 'photos': return play_slideshow(album_id = self.album_id)
    
    #-----------------------
    #   STADIUM METHODS
    #-----------------------
    def get_stadium_visits(self):
        html = _html('http://www.slbenfica.pt/{lang}/estadio/visitas.aspx'.format(lang=self.LANG))
        info = html.find('div', id='dnn_ctr1242_MLHTML_lblContent')
        # title
        title = info.h1
        title.extract()
        # table
        table = info.find('table', class_='pos_tab_generic')
        table.extract()
        table_info = []
        for tr in table.find_all('tr'):
            table_row = filter(None,[td.string for td in tr.find_all('td')])
            table_info.append(table_row)

        if self.KODI:
            # replace </br> with [CR]
            replace_br(info)
            # replace &nbsp; with [CR]
            replace_nbsp(info)

            return {'title': title.string,
                    'text': kodi_text(info),
                    'table': table_info}
        else:
            return {'title': title.string,
                    'text': stringify_text(info),
                    'table': table_info}
            
        

    def get_stadium_info(self):
        html = _html('http://www.slbenfica.pt/{lang}/estadio/estadiodaluz.aspx'.format(lang=self.LANG))
        info = html.find('div', id='dnn_ctr1226_MLHTML_lblContent')
        # title
        title = info.h1
        title.extract()
        # sub-title
        subtitle = info.h2
        subtitle.extract()
        if self.KODI:
            # replace </br> with [CR]
            replace_br(info)
            # replace &nbsp; with [CR]
            replace_nbsp(info)
            # text
            return {'title': title.string.strip(' '),
                    'subtitle': subtitle.string.strip(' '),
                    'text': kodi_text(info)}
        else:
            return {'title': title.string.strip(' '),
                    'subtitle': subtitle.string.strip(' '),
                    'text': stringify_text(info)}


    #-----------------------
    #  CALENDAR METHODS
    #-----------------------
    class Calendar(object):
        
        def __init__(self, startDate=date.today(), numWeeks='1', language='pt-PT', sport_id=None):
    
            self.startDate = startDate
            self.numWeeks = numWeeks
            self.language = language
            self.first_day, self.last_day = Calendar.first_last_day(self.startDate, self.numWeeks, self.language)

        def first_last_day(self, day):
    
            if self.numWeeks:
                end_day = (7 * int(self.numWeeks)) - 1
            
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
    
        def get_calendar(self):
    
            url = 'http://m.slbenfica.pt/HttpHandlers/SLBSportsAgenda.ashx?ModID=1172&LvlId=-1&AgendaStartDate='+self.first_day+'%2000:00:00&NumWeeks='+self.numWeeks+'&CurrentType=Event&Culture='+self.language+'&Mobile=true&PurchaseTicketURL=https://m.slbenfica.pt/'+self.language+'/bilhetes/comprar.aspx'
    
            # convert html to json
            calendar = {}
            sports = []
            sports_events = {}
            events = []
            event  = {}
    
            html_soup = BS(download_page(url).read().decode('utf-8', 'ignore'))
            
            uls = html_soup.find_all('ul', {'class': 'agEvt'})
            lis = [ul.find_all('li') for ul in uls]
    
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
    
            calendar["calendar"] = {"type": "list", "start_date" : self.first_day, "end_date": self.last_day}
    
            for k, v in sports_events.iteritems():
                _id   = get_sport_id(k)
                _name = get_sport_info(_id)[0]
                sports.append({"id": _id, "name": _name, "events": v})
    
            calendar["calendar"]["sports"] = sports
    
            return calendar if calendar else [] 