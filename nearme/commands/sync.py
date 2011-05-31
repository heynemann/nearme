#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nearme geospatial referencing
# https://github.com/heynemann/nearme

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from optparse import OptionParser
from Queue import Queue
from threading import Thread
import time

from mongoengine import connect

from nearme.commands.base import BaseCommand
from nearme.models import Place

class SyncDBCommand(BaseCommand):

    def line_split(self, line):
#geonameid         : integer id of record in geonames database
#name              : name of geographical point (utf8) varchar(200)
#asciiname         : name of geographical point in plain ascii characters, varchar(200)
#alternatenames    : alternatenames, comma separated varchar(5000)
#latitude          : latitude in decimal degrees (wgs84)
#longitude         : longitude in decimal degrees (wgs84)
#feature class     : see http://www.geonames.org/export/codes.html, char(1)
#feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
#country code      : ISO-3166 2-letter country code, 2 characters
#cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
#admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
#admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
#admin3 code       : code for third level administrative division, varchar(20)
#admin4 code       : code for fourth level administrative division, varchar(20)
#population        : bigint (8 byte int) 
#elevation         : in meters, integer
#gtopo30           : average elevation of 30'x30' (ca 900mx900m) area in meters, integer
#timezone          : the timezone id (see file timeZone.txt)
#modification date : date of last modification in yyyy-MM-dd format
        values = line.split('\t')

        return {
            'geonameid': values[0],
            'name': values[1],
            'ascii_name': values[2],
            'alternate_names': values[3].split(','),
            'latitude': float(values[4]),
            'longitude': float(values[5]),
            'feature_class': values[6],
            'feature_code': values[7],
            'country_code': values[8],
            'cc2': values[9].split(','),
            'admin1': values[10],
            'admin2': values[11],
            'admin3': values[12],
            'admin4': values[13],
            'population': values[14],
            'elevation': values[15],
            'gtopo30': values[16],
            'timezone': values[17],
            'mod_date': values[18]
        }
    
    def save_place(self, values):
        place = Place.from_values(values)
        place.save()

    def run(self):
        parser = OptionParser()
        parser.add_option("-d", "--dbhost", dest="dbhost", default="0.0.0.0",
                          help="mongodb host.")
        parser.add_option("-p", "--dbport", type="int", dest="dbport", default=20000,
                          help="mongodb port.")
        parser.add_option("-w", "--workers", type="int", dest="workers", default=10,
                          help="number of workers.")
        parser.add_option('-l', '--verbose', dest='verbose', action='store_true', default=False)

        (opt, args) = parser.parse_args(self.arguments)

        if not args:
            print "Please pass the geo file as last argument"
            return

        connect('nearme', host=opt.dbhost, port=opt.dbport)

        self.available_items = Queue()

        def log(msg):
            if opt.verbose:
                print msg

        for i in range(opt.workers):
            t = Thread(target=self.worker(log))
            t.setDaemon(True)
            t.start()

        data = open(args[0]).read()

        line = []
        for char in data:
            if char == '\n':
                joined = ''.join(line)
                #log('appending "%s" for processing' % joined[:10])
                self.available_items.put(joined)
                line = []
            else:
                line.append(char)

        self.available_items.join()

    def worker(self, log):
        def runner():
            while True:
                if self.available_items.empty():
                    time.sleep(0.1)
                    continue

                line = self.available_items.get()

                values = self.line_split(line)

                log("processing %s" % values['name'])

                self.save_place(values)

                self.available_items.task_done()

        return runner
