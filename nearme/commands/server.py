#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nearme geospatial referencing
# https://github.com/heynemann/nearme

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

from nearme.commands.base import BaseCommand
import tornado.ioloop
import tornado.web
from models import Place
from mongoengine import connect

connect('nearme', port = 20000)

class LookupCities(tornado.web.RequestHandler):
    def get(self, latitude, longitude, limit):
        near_places = Place.objects(point__near = [float(latitude), float(longitude)])[:int(limit)]

        for place in near_places:
           self.write("%s<br>" % place.name)

application = tornado.web.Application([
    ("/find/(.+?)/(.+?)/(\d+)", LookupCities)
])

class ServeCommand(BaseCommand):

    def run(self):
        print "SERVER"

        application.listen(9999)
        tornado.ioloop.IOLoop.instance().start()

