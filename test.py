#!/usr/bin/python
import codecs
from urllib import quote, unquote
import urllib2
from datetime import date, timedelta, datetime
from itertools import chain
from urlparse import urljoin, urlsplit, urlunsplit
import html5lib
from bs4 import BeautifulSoup
from pprint import pprint

try:
    import json
except:
    import simplejson as json

LANG = 'pt-PT'
HOME_URL = 'http://www.slbenfica.pt/{lang}/home.aspx'.format(lang=LANG)
ROOT_URL = 'http://www.slbenfica.pt/'

#------------------------
#  Web related methods
#------------------------
def download_page(url, data=None):
    request = urllib2.Request(url, data)
    request.add_header('Accept-Encoding', 'utf-8')
    response = urllib2.urlopen(request)
    return response

def _full_url(root, url):
    return urljoin(root, fixurl(url))

def _html(url):
    return BeautifulSoup(download_page(fixurl(url)), 'html5lib')

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

import types

def replace_with_newlines(element):
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, types.StringTypes):
            text += elem.strip()
        elif elem.name == 'br':
            text += '\n'
    return text

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

if __name__ == '__main__':

    # foundation
    html = _html('http://www.slbenfica.pt/{lang}/slb/historia/fundacao.aspx'.format(lang=LANG))
    text = html.find('div', id='dnn_ctr664_MLHTML_lblContent')
    h1 = text.find('h1')
    h1.extract() # remove title
    foundation = {'title': h1.string,
                  'img': _full_url(ROOT_URL, html.find('div', class_='main_cont2_bannertop').img['src']),
                  'text': kodi_text(text)}

    # symbols
    html = _html('http://www.slbenfica.pt/{lang}/slb/historia/simbolos.aspx'.format(lang=LANG))
    symbols = html.find('ul', class_='main_cont2_list')
    symbols.extract() # remove list of symbols to get text only
    intro = html.find('div', id='dnn_ctr670_MLHTML_lblContent')
    title1 = intro.find('h1')
    title1.extract()
    title2 = intro.find('h2')
    title2.extract()
    title = ' - '.join([title1.string.encode('utf-8'), title2.string.encode('utf-8')]).decode('utf-8')

    symbol_history = {'title': title, 
                      'text': kodi_text(intro),
                      'symbols': [{'img': _full_url(ROOT_URL, symbol.find('div', class_='main_cont2_list_img').img['src']),
                                   'text': kodi_text(symbol.find('div', class_='main_cont2_list_det'))} 
                                 for symbol in symbols.findAll('li')]}
    
    # presidents
    def get_president_text(president):
        short = kodi_text(president.find('p', class_='description'))
        link = president.find('p', class_='view_more').a['href']
        view_more = _html(link.encode('utf-8'))
        text = ''
        if view_more.find('h2'): 
            info = view_more.find('h2').parent
            tags = ['h1', 'h2', 'a']
            for tag in tags:
                block = info.find(tag) # remove tags from info
                block.extract()
            text = kodi_text(info)
        return {'short': short, 'long': text}

    html = _html('http://www.slbenfica.pt/{lang}/slb/historia/presidentes.aspx'.format(lang=LANG))

    intro = html.find('div', id='dnn_ctr2916_MLHTML_lblContent')
    title = intro.find('h1') # title
    title.extract()
    tags = ['div', 'a']
    for tag in tags:
        block = intro.find(tag) # remove tags from intro
        block.extract()

    presidents = {'title': title.get_text(strip=True),
                  'text': kodi_text(intro),
                  'list': [{'num': index + 1,
                            'period': president.find('p', class_='line_1st').string,
                            'name': president.find('p', class_='line_2nd').string,
                            'description': get_president_text(president)}
                            for index, president in enumerate(html.find('div', class_='modal_window_content clearfix').findAll('div', class_='body'))]}
    
    # honours
    html = _html('http://www.slbenfica.pt/{lang}/slb/historia/condecoracoes.aspx'.format(lang=LANG))
    honours = [{'name': honour.find('h3'),
                'awards': honour.find('p')} for honour in html.findAll('h3')]

    club_history = {'foundation': foundation,
                    'symbols': symbol_history,
                    'presidents': presidents,
                    'honours': honours }

    if club_history:
        with codecs.open('club_history.json', 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(club_history, ensure_ascii=False)))
        f.close()
