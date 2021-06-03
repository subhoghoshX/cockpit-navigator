#!/usr/bin/env python3

"""
    Cockpit Navigator - A File System Browser for Cockpit.
    Copyright (C) 2021 Josh Boudreau <jboudreau@45drives.com>

    This file is part of Cockpit Navigator.
    Cockpit Navigator is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Cockpit Navigator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Cockpit Navigator.  If not, see <https://www.gnu.org/licenses/>.
"""

import base64
import os
import sys
import json

def write_chunk(chunk, file):
    seek = chunk["seek"]
    data = base64.b64decode(chunk["chunk"])
    file.seek(seek)
    file.write(data)

def main():
    if len(sys.argv) != 2:
        print("Invalid number of arguments.")
        sys.exit(1)
    path = sys.argv[1]
    try:
        file = open(path, "a+b")
    except Exception as e:
        print(e)
        sys.exit(1)
    while True:
        try:
            json_in = input()
        except EOFError:
            break
        json_list = json_in.split("\n")
        for json_obj in json_list:
            try:
                obj_in = json.loads(json_obj)
            except Exception as e:
                print(e)
                log = open("/var/log/navigator.log", "w")
                log.write(json_in)
                log.close()
                sys.exit(1)
            write_chunk(obj_in, file)
    file.close()
    sys.exit(0)

if __name__ == "__main__":
    main()