#!/usr/bin/python
import codecs
import urllib2
from datetime import date, timedelta, datetime
from itertools import chain
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup as BS
import pprint

LANG = 'pt-PT'
HOME_URL = 'http://www.slbenfica.pt/{lang}/home.aspx'.format(lang=LANG)

#------------------------
#  Web related methods
#------------------------
def download_page(url, data=None):
    
    proxy = urllib2.ProxyHandler({'http': 'peu141:Jason1981#@ep-proxy.bportugal.pt:8080'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    request = urllib2.Request(url, data)
    request.add_header('Accept-Encoding', 'utf-8')
    response = urllib2.urlopen(request)
    return response

def _full_url(root, url):
    return urljoin(root, url)

def _html(url):
    return BS(download_page(url))

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



if __name__ == '__main__':

    html = _html('http://www.slbenfica.pt/{lang}/clube/org%C3%A3ossociais.aspx'.format(lang=LANG))
    
    club_structure = {}
    
    table = html.find('table', {'class': 'pos_tab_generic'}) 
    # table headers
    header = table.find('tr', {'class': 'tab_top_red'})
    titles = ['board', 'assembly', 'fiscal']

    header.extract() # remove header row from table

    members = [tr.findAll('td') for tr in table.findAll('tr')]

    for idx, title in enumerate(titles): # for each table column
        club_structure[title] = [{'position': member[idx].find('p', {'class': 'txt_11_red'}).string if member[idx].find('p', {'class': 'txt_11_red'}) else '',
                                  'name': member[idx].find('p', {'class': 'txt_11_dark'}).string if member[idx].find('p', {'class': 'txt_11_dark'}) else '',
                                  'affiliate': member[idx].find('p', {'class': 'txt_10'}).string if member[idx].find('p', {'class': 'txt_10'}) else ''}
                                  for member in members]

    pprint.pprint(club_structure)
    
    #COMPETITION = 'dnn_ctr8809_SLBSportsAgendaWidget_RepeaterGames_RepeaterGamesByMainSport_{index}_AgendaWidgetEvent_0_CompetitionNameLit_0'
    #MATCH       = 'dnn_ctr8809_SLBSportsAgendaWidget_RepeaterGames_RepeaterGamesByMainSport_{index}_AgendaWidgetEvent_0_LabelGameDesc_0'
    #MATCH_DATE  = 'dnn_ctr8809_SLBSportsAgendaWidget_RepeaterGames_RepeaterGamesByMainSport_{index}_AgendaWidgetEvent_0_LabelGameDateDesc_0'
    #MATCH_LOCAL = 'dnn_ctr8809_SLBSportsAgendaWidget_RepeaterGames_RepeaterGamesByMainSport_{index}_AgendaWidgetEvent_0_LabelGameLocalDesc_0'
#
    #html = _html(HOME_URL)
    #
    ## Sports id's list
    #sports_lis  = html.find('ul', {'class': 'next_games_categories_menu clearfix'}).findAll('li')
#
    ## Sports next matches
    #matches_uls = html.findAll('ul', {'class': 'next_games_competitions'})
    #matches_lis = [match_ul.findAll('li')[0] for match_ul in matches_uls]
#
    #matches = []
    #for index, match_li in enumerate(matches_lis):
    #    
    #    competition = match_li.find('span', {'id': COMPETITION.format(index=str(index))}).string
    #    match       = match_li.find('span', {'id': MATCH.format(index=str(index))}).string
    #    match_date  = match_li.find('span', {'id': MATCH_DATE.format(index=str(index))}).string
    #    match_local = match_li.find('span', {'id': MATCH_LOCAL.format(index=str(index))}).string
    #    matches.append({'competition': competition, 
    #                    'match': match, 
    #                    'match_date': match_date, 
    #                    'match_local': match_local})    
#
    #next_matches = []
    #for index, sport_li in enumerate(sports_lis):
    #    next_matches.append({'id': int(sport_li.find('a')['id']),
    #                         'sport': get_sport_info(int(sport_li.find('a')['id']))[0],
    #                         'thumbnail': get_sport_info(int(sport_li.find('a')['id']))[1],
    #                         'match_info': {'competition_name' : matches[index]['competition'],
    #                                        'competition_match': matches[index]['match'],
    #                                        'competition_date' : matches[index]['match_date'],
    #                                        'competition_local': matches[index]['match_local']}
    #                        })
    #
    #print next_matches
    