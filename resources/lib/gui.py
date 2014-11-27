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

import xbmc
import xbmcgui
import sys
from traceback import print_exc
import datetime
from resources.lib.base import *
from resources.lib.api import SLB

#-------------------
#  Controls IDs
#-------------------
#class Controls:
#    #--------------
#    #   BUTTONS
#    #--------------
#    MAIN_MENU_CLUB_BUTTON                   = 110
#    MAIN_MENU_NEWS_BUTTON                   = 120
#    MAIN_MENU_VIDEOS_BUTTON                 = 130
#    MAIN_MENU_PHOTOS_BUTTON                 = 140
#    MAIN_MENU_STADIUM_BUTTON                = 150
#    MAIN_MENU_TICKETS_BUTTON                = 160
#    MAIN_MENU_CALENDAR_BUTTON               = 170
#    MAIN_MENU_SPORTS_BTN                    = 180 
#    MAIN_MENU_LIVE_MATCH_BTN                = 190
#    MAIN_MENU_EXIT_BTN                      = 200
#    CLUB_MENU_INFO_BTN                      = 111
#    CLUB_MENU_STRUCTURE_BTN                 = 112
#    CLUB_MENU_HISTORY_BTN                   = 113
#    CLUB_MENU_MUSEUM_BTN                    = 114
#    NEWS_MENU_HEADLINES_BTN                 = 121
#    NEWS_MENU_SPORTS_BTN                    = 122
#    STADIUM_MENU_LIGHT_BTN                  = 151
#    STADIUM_MENU_INFO_BTN                   = 152
#    STADIUM_MENU_TOURS_BTN                  = 153
#    STADIUM_MENU_VIRTUAL_BTN                = 154
#    TICKETS_MENU_MATCHES_BTN                = 161
#    TICKETS_MENU_MATCHES_BTN                = 162
#    CALENDAR_MENU_TODAY_BTN                 = 171
#    CALENDAR_MENU_WEEKLY_BTN                = 172
#    CALENDAR_MENU_MONTHLY_BTN               = 173
#    CALENDAR_NEXT_MATCHES_NEXT_BTN          = 174
#    CALENDAR_NEXT_MATCHES_PREV_BTN          = 175
#    #--------------
#    #   CONTENT
#    #--------------        
#    # CLUB      
#    CONTENT_CLUB_VIEW                       = 9010
#    CONTENT_CLUB_INFO_VIEW                  = 9011
#    CONTENT_CLUB_STRUCTURE_VIEW             = 9012
#    CONTENT_CLUB_HISTORY_VIEW               = 9013
#    CONTENT_CLUB_MUSEUM_VIEW                = 9014
#    # NEWS      
#    CONTENT_NEWS_HEADLINES_VIEW             = 9020
#    CONTENT_NEWS_SPORTS_VIEW                = 9021
#    CONTENT_NEWS_SPORT_VIEW                 = 9022
#    CONTENT_NEWS_ARTICLE_VIEW               = 9023
#    # VIDEOS        
#    CONTENT_VIDEOS_SPORTS_VIEW              = 9031
#    CONTENT_VIDEOS_ALBUMS_VIEW              = 9032
#    CONTENT_ALBUMS_VIDEOS_VIEW              = 9033
#    # PHOTOS        
#    CONTENT_PHOTOS_SPORTS_VIEW              = 9044
#    CONTENT_PHOTOS_ALBUMS_VIEW              = 9045
#    CONTENT_SLIDESHOW_VIEW                  = 9046
#    # STADIUM       
#    CONTENT_STADIUM_LIGHT_VIEW              = 9050
#    CONTENT_STADIUM_INFO_VIEW               = 9051
#    CONTENT_STADIUM_TOURS_VIEW              = 9052
#    CONTENT_STADIUM_VIRTUAL_VIEW            = 9053
#    # TICKETS       
#    CONTENT_TICKETS_MATCHES_VIEW            = 9060
#    CONTENT_TICKETS_MUSEUM_VIEW             = 9061
#    # CALENDAR
#    CONTENT_CALENDAR_NEXT_MATCHES_VIEW      = 9070
#    CONTENT_CALENDAR_TODAY_VIEW             = 9071
#    CONTENT_CALENDAR_WEEKLY_VIEW            = 9072
#    CONTENT_CALENDAR_MONTHLY_VIEW           = 9073
#    CONTENT_CALENDAR_SPORTS_VIEW            = 9074
#    CONTENT_CALENDAR_SPORT_EVENTS_VIEW      = 9075
#    CONTENT_CALENDAR_NEXT_MATCHES_LIST      = 9076
#    # SPORTS
#    CONTENT_SPORTS_VIEW                     = 9080
#    CONTENT_SPORTS_INFO_VIEW                = 9081
#    CONTENT_SPORTS_INFO_DATA_VIEW           = 9082
#    # LIVE MATCHES
#    CONTENT_LIVE_MATCHES_CONTAINER_VIEW     = 9090
#    CONTENT_LIVE_MATCHES_VIEW               = 9091
#    CONTENT_LIVE_MATCHES_LIST_VIEW          = 9092
#    # PANEL
#    CONTENT_PANEL_VIEW                      = 9100
#    CONTENT_SPORT_ALBUMS_LIST               = 9032

class GUI(xbmcgui.WindowXML):

    def __init__(self, *args, **kwargs):
        self.SLB = SLB(kodi=True)

    def onInit(self):
        # Next Matches
        self.next_matches_list = self.getControl(Controls.CONTENT_CALENDAR_NEXT_MATCHES_LIST)
        self.next_matches = self.SLB.get_next_matches()
        self.poulate_next_matches()
        # video sports initialization
        self.video_sports_menu_list = self.getControl(Controls.CONTENT_CALENDAR_NEXT_MATCHES_LIST)
        self.video_sports = self.SLB.get_sports('videos')
        self.populate_video_sports_menu_list

    def onClick(self, controlID):
        # EXIT BUTTON
        if controlID == Controls.MAIN_MENU_EXIT_BTN:
            self.close()
        # Club Navigation
        elif controlID == Controls.CLUB_MENU_STRUCTURE_BTN:
            self.club_structure = self.SLB.get_club_structure()
        # Videos Navigation
        elif controlID in [131, 231, 232, 132, 133, 134, 135, 136, 137, 138, 139, 230]:
            sport_id = self.getControl(Controls.CONTENT_PANEL_VIEW).getProperty(sport_id)
            lw.log([sport_id])
            self.sport_video_albums = self.SLB.get_category_albums(media_type='videos', category_id=sport_id)

    def onAction(self, action):
        pass

    def onFocus(self, controlID):
        pass

    def poulate_next_matches(self):
        
        for index, next_match in enumerate(self.next_matches):
            
            # create new listitem
            match_item = xbmcgui.ListItem()
            # sport name as label
            match_item.setLabel(next_match['sport'])
            # sport competition + match + date + local
            match_item.setProperty('competition_name', next_match['match_info']['competition_name'])
            # sport match home team
            match_item.setProperty('competition_home_team', next_match['match_info']['competition_home_team'])
            # sport match away team
            match_item.setProperty('competition_away_team', next_match['match_info']['competition_away_team'])
            # sport date
            match_item.setProperty('competition_date', next_match['match_info']['competition_date'])
            # sport local
            match_item.setProperty('competition_local', next_match['match_info']['competition_local'])
            # sport image as thumbnail
            match_item.setThumbnailImage(os.path.join(Addon.__imagespath__, next_match['thumbnail']))
            #lw.log([next_match['sport'], os.path.join(Addon.__imagespath__, next_match['thumbnail']), next_match['match_info']['competition_name'], next_match['match_info']['competition_home_team'],  next_match['match_info']['competition_away_team'], next_match['match_info']['competition_date'], next_match['match_info']['competition_local']])
            self.next_matches_list.addItem(match_item)

    def populate_video_sports_menu_list(self):

        for sport in self.video_sports:

    def populate_sport_albums_list(self):

        self.sport_albums_list = self.getControl(Controls.CONTENT_SPORT_ALBUMS_LIST)

        for album in self.sport_video_albums:
            album_item = xbmcgui.ListItem()
            album_item.setLabel(set_color(album['name'], 'red'))
            album_item.setLabel2(album['competition'])
            album_item.setThumbnailImage(album['img'])
            self.sport_albums_list.addItem(album_item)