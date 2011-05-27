#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nearme geospatial referencing
# https://github.com/heynemann/nearme

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

class BaseCommand(object):
    def __init__(self, all_commands, arguments):
        self.all_commands = all_commands
        self.arguments = arguments
