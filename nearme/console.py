#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nearme geospatial referencing
# https://github.com/heynemann/nearme

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 Bernardo Heynemann heynemann@gmail.com

import sys

from nearme.commands.help import HelpCommand
from nearme.commands.sync import SyncDBCommand
from nearme.commands.server import ServeCommand

COMMANDS = {
    'help': HelpCommand,
    'syncdb': SyncDBCommand,
    'serve': ServeCommand
}

def main():
    arguments = sys.argv
    if len(sys.argv) == 1:
        command = "help"
        arguments = []
    else:
        command = arguments[1]
        if len(arguments) > 2:
            arguments = arguments[2:]
        else:
            arguments = []

    command_cls = COMMANDS[command]
    command_cls(COMMANDS, arguments).run()

if __name__ == '__main__':
    main()
