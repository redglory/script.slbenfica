#!/usr/bin/python
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

import codecs
import urllib2
from datetime import date, timedelta, datetime
from itertools import chain
from urlparse import urljoin
from bs4 import BeautifulSoup as BS
import unicodedata
from resources.lib.api import SLB, Calendar

try:
    import json
except:
    import simplejson as json
        
if __name__ == '__main__':
    
    _startdate = date(2014, 11, 03)
    calendar = Calendar.get_calendar(startDate=_startdate, numWeeks='2', language="es-ES")
    if calendar:
        with codecs.open('calendar.json', "w", encoding='utf-8') as f:
            f.write(unicode(json.dumps(calendar, ensure_ascii=False)))
        f.close()
    else:   
        print "No response"