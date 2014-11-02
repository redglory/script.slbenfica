import xbmc
import xbmcgui
import sys
from traceback import print_exc
import datetime

class GUI(xbmcgui.WindowXML):

    def __init__( self, *args, **kwargs ):
        pass

    def onInit( self ):
        pass

    def onClick( self, controlID ):
        if controlID == 200: # Exit Button
            self.close()

    def onAction( self, action ):
        pass

    def onFocus( self, controlID ):
        pass