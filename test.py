#!/usr/bin/python
import sys, re, os
from urlparse import urlparse, parse_qs, urljoin, urlsplit, urlunsplit
from itertools import chain
import time
from urllib import quote, unquote
import urllib2
import codecs
from datetime import date, timedelta, datetime
import unicodedata
from pprint import pprint

try:
    import json
except:
    import simplejson as json

from bs4 import BeautifulSoup, NavigableString, Tag

LANG       = 'pt-PT'
HOME_URL   = 'http://www.slbenfica.pt/{lang}/home.aspx'.format(lang=LANG)
ROOT_URL   = 'http://www.slbenfica.pt/'
VIDEOS_URL = 'http://www.slbenfica.pt/{lang}/videos.aspx'.format(lang=LANG)
PHOTOS_URL = 'http://www.slbenfica.pt/{lang}/fotos.aspx'.format(lang=LANG)

class Addon:
    __imagespath__ = os.path.join(u'C:\\Users\\peu141\\AppData\\Roaming\\XBMC\\addons\\script.slbenfica\\resources\\images\\'.encode('utf-8')).decode( "utf-8" )

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

def translate_sport(sport):
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

def get_sport_info(sport_id):

    # [id]: (sport_name, img)
    return{
            18    :('NOME DESPORTO 1', "Handball.png"),
            20    :('NOME DESPORTO 2', "Martial Arts.png"),
            19    :('NOME DESPORTO 3', "Athletics.png"),
            2781  :('NOME DESPORTO 4', "Racing.png"),
            2132  :('NOME DESPORTO 5', "Club.png"),
            17    :('NOME DESPORTO 6', "Basketball.png"),
            21    :('NOME DESPORTO 7', "Billiard.png"),
            22    :('NOME DESPORTO 8', "Canoeing.png"),              
            44    :('NOME DESPORTO 9', "Club.png"),
            23    :('NOME DESPORTO 10', "Boxing.png"),
            37    :('NOME DESPORTO 11', "Team.png"),
            39    :('NOME DESPORTO 12', "Team.png"),
            38    :('NOME DESPORTO 13', "Team.png"),
            1707  :('NOME DESPORTO 14', "FunZone.png"),
            12    :('NOME DESPORTO 15', "Football.png"),               
            14    :('NOME DESPORTO 16', "Football.png"),                
            1614  :('NOME DESPORTO 17', "Other.png"),                 
            24    :('NOME DESPORTO 18', "Gymnastics.png"),
            25    :('NOME DESPORTO 19', "Golf.png"),        
            16    :('NOME DESPORTO 20', "Hockey.png"),                
            1814  :('NOME DESPORTO 21', "Hockey.png"),                
            46    :('NOME DESPORTO 22', "Olympic Games.png"),
            26    :('NOME DESPORTO 23', "Judo.png"),                  
            41    :('NOME DESPORTO 24', "Swimming.png"),  
            45    :('NOME DESPORTO 25', "Other.png"),
            34    :('NOME DESPORTO 26', "Paintball.png"),          
            28    :('NOME DESPORTO 27', "Sport Fishing.png"),
            40    :('NOME DESPORTO 28', "Team.png"), 
            29    :('NOME DESPORTO 29', "Rugby.png"),      
            2030  :('NOME DESPORTO 30', "Rugby.png"),
            1914  :('NOME DESPORTO 31', "Club.png"),        
            31    :('NOME DESPORTO 32', "Table Tennis.png"),         
            33    :('NOME DESPORTO 33', "Triathlon.png"),
            15    :('NOME DESPORTO 34', "Volleyball.png"),              
            2190  :('NOME DESPORTO 35', "Chess.png")
    }[sport_id]


def get_cat_id(url, otype):

    pattern = '/cat/(.*?)/'
    match = re.search(pattern, url)
    return match.group(1)

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
    return BeautifulSoup(download_page(fixurl(url)), 'html5lib')

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

def kodi_text(text):
    pretty_text = [line for line in text.stripped_strings]
    return u'\n'.encode('utf-8').join(pretty_text)

if __name__ == '__main__':

    html = _html('http://www.slbenfica.pt/{lang}/estadio/visitas.aspx'.format(lang=LANG))
    info = html.find('div', id='dnn_ctr1242_MLHTML_lblContent')
    # title
    title = info.h1
    title.extract()
    # clean </br>
    for br in info.find_all('br'):
        br.extract()
    # table
    table = info.find('table', class_='pos_tab_generic')
    table.extract()
    table_info = []
    for tr in table.find_all('tr'):
        table_row = filter(None,[td.string for td in tr.find_all('td')])
        table_info.append(table_row)
        
    stadium_visits = {'text': kodi_text(info),
                      'table': table_info}

    if stadium_visits:
        pprint(stadium_visits)
        #with codecs.open('stadium_visits.json', "w", encoding='utf-8') as f:
        #    f.write(unicode(json.dumps(stadium_visits, ensure_ascii=False), 'utf8'))
        #f.close()#