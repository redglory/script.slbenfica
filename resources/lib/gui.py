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
#    CONTENT_CLUB_PANEL                      = 9010
#    CONTENT_CLUB_INFO_PANEL                 = 9011
#    CONTENT_CLUB_STRUCTURE_PANEL            = 9012
#    CONTENT_CLUB_HISTORY_PANEL              = 9013
#    CONTENT_CLUB_MUSEUM_PANEL               = 9014
#    # NEWS      
#    CONTENT_NEWS_HEADLINES_PANEL            = 9020
#    CONTENT_NEWS_SPORTS_PANEL               = 9021
#    CONTENT_NEWS_SPORT_PANEL                = 9022
#    CONTENT_NEWS_ARTICLE_PANEL              = 9023
#    # VIDEOS        
#    CONTENT_VIDEOS_SPORTS_PANEL             = 9030
#    CONTENT_VIDEOS_SPORTS_LIST              = 9031
#    CONTENT_VIDEOS_SPORT_ALBUMS_PANEL       = 9032
#    CONTENT_VIDEOS_SPORT_ALBUMS_LIST        = 9033
#    CONTENT_ALBUMS_VIDEOS_PANEL             = 9034
#    CONTENT_ALBUMS_VIDEOS_LIST              = 9035
#    # PHOTOS        
#    CONTENT_PHOTOS_SPORTS_PANEL             = 9040
#    CONTENT_PHOTOS_SPORTS_LIST              = 9041
#    CONTENT_PHOTOS_SPORT_ALBUMS_PANEL       = 9042
#    CONTENT_PHOTOS_SPORT_ALBUMS_LIST        = 9043
#    CONTENT_SLIDESHOW_PANEL                 = 9044
#    CONTENT_SLIDESHOW_LIST                  = 9045
#    # STADIUM       
#    CONTENT_STADIUM_LIGHT_PANEL             = 9050
#    CONTENT_STADIUM_INFO_PANEL              = 9051
#    CONTENT_STADIUM_TOURS_PANEL             = 9052
#    CONTENT_STADIUM_VIRTUAL_PANEL           = 9053
#    # TICKETS       
#    CONTENT_TICKETS_MATCHES_PANEL           = 9060
#    CONTENT_TICKETS_MUSEUM_PANEL            = 9061
#    # CALENDAR
#    CONTENT_CALENDAR_NEXT_MATCHES_PANEL     = 9070
#    CONTENT_CALENDAR_TODAY_PANEL            = 9071
#    CONTENT_CALENDAR_WEEKLY_PANEL           = 9072
#    CONTENT_CALENDAR_MONTHLY_PANEL          = 9073
#    CONTENT_CALENDAR_SPORTS_PANEL           = 9074
#    CONTENT_CALENDAR_SPORT_EVENTS_PANEL     = 9075
#    CONTENT_CALENDAR_NEXT_MATCHES_LIST      = 9076
#    # SPORTS
#    CONTENT_SPORTS_PANEL                    = 9080
#    CONTENT_SPORTS_INFO_PANEL               = 9081
#    CONTENT_SPORTS_INFO_DATA_PANEL          = 9082
#    # LIVE MATCHES
#    CONTENT_LIVE_MATCHES_CONTAINER_PANEL    = 9090
#    CONTENT_LIVE_MATCHES_PANEL              = 9091
#    CONTENT_LIVE_MATCHES_LIST_PANEL         = 9092
#    # PANEL
#    CONTENT_PANEL_PANEL                     = 9100
class GUI(xbmcgui.WindowXML):

    def __init__(self, *args, **kwargs):
        self.SLB = SLB(kodi=True)

    def onInit(self):
        # Next Matches
        self.next_matches_list = self.getControl(Controls.CONTENT_CALENDAR_NEXT_MATCHES_LIST)
        self.next_matches = self.SLB.get_next_matches()
        self.set_next_matches()
        # video sports initialization


    def onClick(self, controlID):
        # EXIT BUTTON
        if controlID == Controls.MAIN_MENU_EXIT_BTN:
            self.close()
        # Club Navigation
        elif controlID == Controls.CLUB_MENU_STRUCTURE_BTN:
            self.club_structure = self.SLB.get_club_structure()
        # Video Sports
        elif controlID == Controls.MAIN_MENU_VIDEOS_BUTTON:        
            self.videos_sports_list = self.getControl(Controls.CONTENT_VIDEOS_SPORTS_LIST)
            self.videos_sports_list.reset()
            self.videos_sports = self.SLB.get_sports('videos')
            self.set_videos_sports_list(self.videos_sports)
            self.setFocus(self.videos_sports_list)
            self.videos_sports_list.selectItem(0)
        # Videos Sport Albums Navigation
        elif controlID == Controls.CONTENT_VIDEOS_SPORTS_LIST:
            sport_id = self.getControl(controlID).getSelectedItem().getProperty('sport_id')
            self.sport_albums_list = self.getControl(Controls.CONTENT_VIDEOS_SPORT_ALBUMS_LIST)
            self.sport_video_albums = self.SLB.get_sport_albums(media_type='videos', sport_id=sport_id)
            self.set_sport_albums_list(self.sport_video_albums)
            self.setFocus(self.sport_albums_list)
            self.sport_albums_list.selectItem(0)


    def onAction(self, action):
        pass

    def onFocus(self, controlID):
        pass

    def set_next_matches(self):
        
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
            match_item.setIconImage(os.path.join(Addon.__imagespath__, next_match['thumbnail']))
            match_item.setThumbnailImage(os.path.join(Addon.__imagespath__, next_match['thumbnail']))
            #lw.log([next_match['sport'], os.path.join(Addon.__imagespath__, next_match['thumbnail']), next_match['match_info']['competition_name'], next_match['match_info']['competition_home_team'],  next_match['match_info']['competition_away_team'], next_match['match_info']['competition_date'], next_match['match_info']['competition_local']])
            self.next_matches_list.addItem(match_item)

    def set_videos_sports_list(self, videos_sports):

        for sport in videos_sports:
            sport_item = xbmcgui.ListItem()
            sport_item.setProperty('sport_id', sport['id'])
            sport_item.setLabel(sport['name'])
            sport_item.setIconImage(sport['img'])
            sport_item.setThumbnailImage(sport['img'])
            self.videos_sports_list.addItem(sport_item)

    def set_sport_albums_list(self, sport_video_albums):

        for album in sport_video_albums:
            album_item = xbmcgui.ListItem()
            album_item.setLabel(set_color(album['name'], 'red'))
            album_item.setLabel2(album['competition'])
            album_item.setIconImage(album['img'])
            album_item.setThumbnailImage(album['img'])
            self.sport_albums_list.addItem(album_item)