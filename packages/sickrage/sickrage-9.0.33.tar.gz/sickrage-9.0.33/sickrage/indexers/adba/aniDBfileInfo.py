#
# This file is part of aDBa.
#
# aDBa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# aDBa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with aDBa.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, with_statement

import hashlib
import io
import os
import time
from xml.etree.ElementTree import ElementTree

import sickrage


def get_file_hash(filePath):
    """ Returns the ed2k hash of a given file."""
    if not filePath:
        return None
    md4 = hashlib.new('md4').copy

    def gen(f):
        while True:
            x = f.read(9728000)
            if x:
                yield x
            else:
                return

    def md4_hash(data):
        m = md4()
        m.update(data)
        return m

    with io.open(filePath, 'rb') as f:
        a = gen(f)
        hashes = [md4_hash(data).digest() for data in a]
        if len(hashes) == 1:
            return hashes[0].encode("hex")
        else:
            return md4_hash(reduce(lambda a, d: a + d, hashes, "")).hexdigest()


def get_file_size(path):
    size = os.path.getsize(path)
    return size


def _remove_file_failed(file):
    try:
        os.remove(file)
    except:
        pass


def get_anime_titles_xml(path):
    return sickrage.srCore.srWebSession.download(
        "https://raw.githubusercontent.com/ScudLee/anime-lists/master/animetitles.xml", path)


def get_anime_list_xml(path):
    return sickrage.srCore.srWebSession.download(
        "https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-list.xml", path)


def read_anidb_xml(filePath=None):
    if not filePath:
        filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animetitles.xml")

    if not os.path.isfile(filePath):
        if not get_anime_titles_xml(filePath):
            return
    else:
        mtime = os.path.getmtime(filePath)
        if time.time() > mtime + 24 * 60 * 60:
            if not get_anime_titles_xml(filePath):
                return

    return read_xml_into_etree(filePath)


def read_tvdb_map_xml(filePath=None):
    if not filePath:
        filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anime-list.xml")

    if not os.path.isfile(filePath):
        if not get_anime_list_xml(filePath):
            return
    else:
        mtime = os.path.getmtime(filePath)
        if time.time() > mtime + 24 * 60 * 60:
            if not get_anime_list_xml(filePath):
                return

    return read_xml_into_etree(filePath)


def read_xml_into_etree(filePath):
    if not filePath:
        return None

    with io.open(filePath, "r") as f:
        return ElementTree(file=f)
