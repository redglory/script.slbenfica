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

#----------------------------------------
#   LIBRARIES & GLOBALS DECLARATIONS
#----------------------------------------
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

# Custom includes
from resources.lib.base import *
from resources.lib.api import SLB, Calendar


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



#----------------------
#    PATH INCLUDE
#----------------------
sys.path = [__resource__] + sys.path

#----------------------
#     GUI CLASS
#----------------------
from gui import GUI
#----------------------
#     LOG CLASS
#----------------------
from xlogger import Logger

lw = Logger(preamble=__preamble__)


#-----------------------
#   Slideshow methods
#-----------------------
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


#-----------------------
#         MAIN
#-----------------------

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
        
#-----------------------