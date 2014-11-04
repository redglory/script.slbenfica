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
sys.path.append(Addon.__libs__)
#----------------------
#     GUI CLASS
#----------------------
from gui import SLB

#-----------------------
#     MAIN CLASS
#-----------------------
class Main:
    def __init__(self):

        # create reset window properties
        xbmcgui.Window( 10000 ).setProperty( "slbenfica_addon_running", "False" )
        self._parse_argv()
        if xbmcgui.Window( 10000 ).getProperty( "slbenfica_addon_running" ) == "True":
            lw.log(["SL Benfica Addon already running, exiting..."], xbmc.LOGNOTICE )
        else:
            xbmcgui.Window( 10000 ).setProperty( "slbenfica_addon_running", "True" )
            self._init_window()

    def _parse_argv( self ):

        try:
            params = dict( arg.split( "=" ) for arg in sys.argv[ 1 ].split( "&" ) )
        except IndexError:
            params = {}        
        except Exception, e:
            lw.log( ['unexpected error while parsing arguments', e] )
            params = {}

    def _init_window(self):
        try:
            lw.log( ["############################################################"], xbmc.LOGNOTICE )
            lw.log( ["#    %-50s    #" % Addon.__name__], xbmc.LOGNOTICE )
            lw.log( ["#    %-50s    #" % Addon.__id__], xbmc.LOGNOTICE )
            lw.log( ["#    %-50s    #" % Addon.__author__], xbmc.LOGNOTICE )
            lw.log( ["#    %-50s    #" % Addon.__version__], xbmc.LOGNOTICE )
            lw.log( ["############################################################"], xbmc.LOGNOTICE )
    
            slbWindow = SLB( "script-slbenfica.xml" , Addon.__path__, "Default")
            slbWindow.doModal()
            del slbWindow
        except:
            lw.log(['Error in script occured:', print_exc()])
            xbmcgui.Window( 10000 ).setProperty( "slbenfica_addon_running", "False" )

    def _get_settings( self ):
        #getSetting()
        pass

#-----------------------
#         MAIN
#-----------------------
if ( __name__ == "__main__" ):
    
    slbenfica = Main()

#-----------------------