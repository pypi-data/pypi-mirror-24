# Author: echel0n <tv@gmail.com>
# URL: https://tv
# Git: https://github.com/V/git
#
# This file is part of 
#
# is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with   If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import base64
import datetime
import os
import os.path
import pickle
import re
import sys
import uuid
from itertools import izip, cycle

from configobj import ConfigObj

import sickrage
from sickrage.core.classes import srIntervalTrigger
from sickrage.core.common import SD, WANTED, SKIPPED, Quality
from sickrage.core.helpers import backupVersionedFile, makeDir, generateCookieSecret, autoType, get_lan_ip


class srConfig(object):
    def __init__(self):
        self.loaded = False

        self.CONFIG_OBJ = None
        self.CONFIG_VERSION = 11
        self.ENCRYPTION_VERSION = 0
        self.ENCRYPTION_SECRET = ""

        self.LAST_DB_COMPACT = 0

        self.CENSORED_ITEMS = {}

        self.NAMING_EP_TYPE = ("%(seasonnumber)dx%(episodenumber)02d",
                               "s%(seasonnumber)02de%(episodenumber)02d",
                               "S%(seasonnumber)02dE%(episodenumber)02d",
                               "%(seasonnumber)02dx%(episodenumber)02d")
        self.SPORTS_EP_TYPE = ("%(seasonnumber)dx%(episodenumber)02d",
                               "s%(seasonnumber)02de%(episodenumber)02d",
                               "S%(seasonnumber)02dE%(episodenumber)02d",
                               "%(seasonnumber)02dx%(episodenumber)02d")
        self.NAMING_EP_TYPE_TEXT = ("1x02", "s01e02", "S01E02", "01x02")
        self.NAMING_MULTI_EP_TYPE = {0: ["-%(episodenumber)02d"] * len(self.NAMING_EP_TYPE),
                                     1: [" - " + x for x in self.NAMING_EP_TYPE],
                                     2: [x + "%(episodenumber)02d" for x in ("x", "e", "E", "x")]}
        self.NAMING_MULTI_EP_TYPE_TEXT = ("extend", "duplicate", "repeat")
        self.NAMING_SEP_TYPE = (" - ", " ")
        self.NAMING_SEP_TYPE_TEXT = (" - ", "space")

        self.LOG_DIR = ""
        self.LOG_FILE = ""
        self.LOG_SIZE = 1048576
        self.LOG_NR = 5
        self.VERSION_NOTIFY = False
        self.AUTO_UPDATE = False
        self.NOTIFY_ON_UPDATE = False
        self.PIP_PATH = ""
        self.GIT_RESET = True
        self.GIT_USERNAME = ""
        self.GIT_PASSWORD = ""
        self.GIT_PATH = ""
        self.GIT_AUTOISSUES = False
        self.GIT_NEWVER = False
        self.CHANGES_URL = 'https://git.sickrage.ca/SiCKRAGE/sickrage/raw/master/changelog.md'
        self.SOCKET_TIMEOUT = 30
        self.WEB_HOST = ""
        self.WEB_PORT = None
        self.WEB_LOG = False
        self.WEB_ROOT = None
        self.WEB_USERNAME = None
        self.WEB_PASSWORD = None
        self.WEB_IPV6 = False
        self.WEB_COOKIE_SECRET = None
        self.WEB_USE_GZIP = True
        self.HANDLE_REVERSE_PROXY = False
        self.PROXY_SETTING = None
        self.PROXY_INDEXERS = True
        self.SSL_VERIFY = True
        self.ENABLE_HTTPS = False
        self.HTTPS_CERT = None
        self.HTTPS_KEY = None
        self.API_KEY = None
        self.API_ROOT = None
        self.INDEXER_DEFAULT_LANGUAGE = None
        self.EP_DEFAULT_DELETED_STATUS = None
        self.LAUNCH_BROWSER = False
        self.SHOWUPDATE_STALE = True
        self.ROOT_DIRS = None
        self.CPU_PRESET = None
        self.ANON_REDIRECT = None
        self.DOWNLOAD_URL = None
        self.TRASH_REMOVE_SHOW = False
        self.TRASH_ROTATE_LOGS = False
        self.SORT_ARTICLE = False
        self.DISPLAY_ALL_SEASONS = True
        self.DEFAULT_PAGE = None
        self.USE_LISTVIEW = False

        self.QUALITY_DEFAULT = None
        self.STATUS_DEFAULT = None
        self.STATUS_DEFAULT_AFTER = None
        self.FLATTEN_FOLDERS_DEFAULT = False
        self.SUBTITLES_DEFAULT = False
        self.INDEXER_DEFAULT = None
        self.INDEXER_TIMEOUT = None
        self.SCENE_DEFAULT = False
        self.ANIME_DEFAULT = False
        self.ARCHIVE_DEFAULT = False
        self.NAMING_MULTI_EP = False
        self.NAMING_ANIME_MULTI_EP = False
        self.NAMING_PATTERN = None
        self.NAMING_ABD_PATTERN = None
        self.NAMING_CUSTOM_ABD = False
        self.NAMING_SPORTS_PATTERN = None
        self.NAMING_CUSTOM_SPORTS = False
        self.NAMING_ANIME_PATTERN = None
        self.NAMING_CUSTOM_ANIME = False
        self.NAMING_FORCE_FOLDERS = False
        self.NAMING_STRIP_YEAR = False
        self.NAMING_ANIME = None
        self.USE_NZBS = False
        self.USE_TORRENTS = False
        self.NZB_METHOD = None
        self.NZB_DIR = None
        self.USENET_RETENTION = 500
        self.TORRENT_METHOD = None
        self.TORRENT_DIR = None
        self.DOWNLOAD_PROPERS = False
        self.ENABLE_RSS_CACHE = True
        self.PROPER_SEARCHER_INTERVAL = None
        self.ALLOW_HIGH_PRIORITY = False
        self.SAB_FORCED = False
        self.RANDOMIZE_PROVIDERS = False
        self.MIN_AUTOPOSTPROCESSOR_FREQ = 1
        self.MIN_NAMECACHE_FREQ = 1
        self.MIN_DAILY_SEARCHER_FREQ = 10
        self.MIN_BACKLOG_SEARCHER_FREQ = 10
        self.MIN_VERSION_UPDATER_FREQ = 1
        self.MIN_SUBTITLE_SEARCHER_FREQ = 1
        self.BACKLOG_DAYS = 7
        self.ADD_SHOWS_WO_DIR = False
        self.CREATE_MISSING_SHOW_DIRS = False
        self.RENAME_EPISODES = False
        self.AIRDATE_EPISODES = False
        self.FILE_TIMESTAMP_TIMEZONE = None
        self.PROCESS_AUTOMATICALLY = False
        self.NO_DELETE = False
        self.KEEP_PROCESSED_DIR = False
        self.PROCESS_METHOD = None
        self.DELRARCONTENTS = False
        self.MOVE_ASSOCIATED_FILES = False
        self.POSTPONE_IF_SYNC_FILES = True
        self.NFO_RENAME = True
        self.TV_DOWNLOAD_DIR = None
        self.UNPACK = False
        self.SKIP_REMOVED_FILES = False
        self.NZBS = False
        self.NZBS_UID = None
        self.NZBS_HASH = None
        self.OMGWTFNZBS = False
        self.NEWZBIN = False
        self.NEWZBIN_USERNAME = None
        self.NEWZBIN_PASSWORD = None
        self.SAB_USERNAME = None
        self.SAB_PASSWORD = None
        self.SAB_APIKEY = None
        self.SAB_CATEGORY = None
        self.SAB_CATEGORY_BACKLOG = None
        self.SAB_CATEGORY_ANIME = None
        self.SAB_CATEGORY_ANIME_BACKLOG = None
        self.SAB_HOST = None
        self.NZBGET_USERNAME = None
        self.NZBGET_PASSWORD = None
        self.NZBGET_CATEGORY = None
        self.NZBGET_CATEGORY_BACKLOG = None
        self.NZBGET_CATEGORY_ANIME = None
        self.NZBGET_CATEGORY_ANIME_BACKLOG = None
        self.NZBGET_HOST = None
        self.NZBGET_USE_HTTPS = False
        self.NZBGET_PRIORITY = 100
        self.TORRENT_USERNAME = None
        self.TORRENT_PASSWORD = None
        self.TORRENT_HOST = None
        self.TORRENT_PATH = None
        self.TORRENT_SEED_TIME = None
        self.TORRENT_PAUSED = False
        self.TORRENT_HIGH_BANDWIDTH = False
        self.TORRENT_LABEL = None
        self.TORRENT_LABEL_ANIME = None
        self.TORRENT_VERIFY_CERT = False
        self.TORRENT_RPCURL = None
        self.TORRENT_AUTH_TYPE = None
        self.TORRENT_TRACKERS = "udp://coppersurfer.tk:6969/announce," \
                                "udp://open.demonii.com:1337," \
                                "udp://exodus.desync.com:6969," \
                                "udp://9.rarbg.me:2710/announce," \
                                "udp://glotorrents.pw:6969/announce," \
                                "udp://tracker.openbittorrent.com:80/announce," \
                                "udp://9.rarbg.to:2710/announce"
        self.USE_KODI = False
        self.KODI_ALWAYS_ON = True
        self.KODI_NOTIFY_ONSNATCH = False
        self.KODI_NOTIFY_ONDOWNLOAD = False
        self.KODI_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.KODI_UPDATE_LIBRARY = False
        self.KODI_UPDATE_FULL = False
        self.KODI_UPDATE_ONLYFIRST = False
        self.KODI_HOST = None
        self.KODI_USERNAME = None
        self.KODI_PASSWORD = None
        self.USE_PLEX = False
        self.PLEX_NOTIFY_ONSNATCH = False
        self.PLEX_NOTIFY_ONDOWNLOAD = False
        self.PLEX_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.PLEX_UPDATE_LIBRARY = False
        self.PLEX_SERVER_HOST = None
        self.PLEX_SERVER_TOKEN = None
        self.PLEX_HOST = None
        self.PLEX_USERNAME = None
        self.PLEX_PASSWORD = None
        self.USE_PLEX_CLIENT = False
        self.PLEX_CLIENT_USERNAME = None
        self.PLEX_CLIENT_PASSWORD = None
        self.USE_EMBY = False
        self.EMBY_HOST = None
        self.EMBY_APIKEY = None
        self.USE_GROWL = False
        self.GROWL_NOTIFY_ONSNATCH = False
        self.GROWL_NOTIFY_ONDOWNLOAD = False
        self.GROWL_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.GROWL_HOST = None
        self.GROWL_PASSWORD = None
        self.USE_FREEMOBILE = False
        self.FREEMOBILE_NOTIFY_ONSNATCH = False
        self.FREEMOBILE_NOTIFY_ONDOWNLOAD = False
        self.FREEMOBILE_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.FREEMOBILE_ID = None
        self.FREEMOBILE_APIKEY = None
        self.USE_PROWL = False
        self.PROWL_NOTIFY_ONSNATCH = False
        self.PROWL_NOTIFY_ONDOWNLOAD = False
        self.PROWL_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.PROWL_API = None
        self.PROWL_PRIORITY = False
        self.USE_TWITTER = False
        self.TWITTER_NOTIFY_ONSNATCH = False
        self.TWITTER_NOTIFY_ONDOWNLOAD = False
        self.TWITTER_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.TWITTER_USERNAME = None
        self.TWITTER_PASSWORD = None
        self.TWITTER_PREFIX = None
        self.TWITTER_DMTO = None
        self.TWITTER_USEDM = False
        self.USE_BOXCAR = False
        self.BOXCAR_NOTIFY_ONSNATCH = False
        self.BOXCAR_NOTIFY_ONDOWNLOAD = False
        self.BOXCAR_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.BOXCAR_USERNAME = None
        self.BOXCAR_PASSWORD = None
        self.BOXCAR_PREFIX = None
        self.USE_BOXCAR2 = False
        self.BOXCAR2_NOTIFY_ONSNATCH = False
        self.BOXCAR2_NOTIFY_ONDOWNLOAD = False
        self.BOXCAR2_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.BOXCAR2_ACCESSTOKEN = None
        self.USE_PUSHOVER = False
        self.PUSHOVER_NOTIFY_ONSNATCH = False
        self.PUSHOVER_NOTIFY_ONDOWNLOAD = False
        self.PUSHOVER_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.PUSHOVER_USERKEY = None
        self.PUSHOVER_APIKEY = None
        self.PUSHOVER_DEVICE = None
        self.PUSHOVER_SOUND = None
        self.USE_LIBNOTIFY = False
        self.LIBNOTIFY_NOTIFY_ONSNATCH = False
        self.LIBNOTIFY_NOTIFY_ONDOWNLOAD = False
        self.LIBNOTIFY_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.USE_NMJ = False
        self.NMJ_HOST = None
        self.NMJ_DATABASE = None
        self.NMJ_MOUNT = None
        self.ANIMESUPPORT = False
        self.USE_ANIDB = False
        self.ANIDB_USERNAME = None
        self.ANIDB_PASSWORD = None
        self.ANIDB_USE_MYLIST = False
        self.ANIME_SPLIT_HOME = False
        self.USE_SYNOINDEX = False
        self.USE_NMJv2 = False
        self.NMJv2_HOST = None
        self.NMJv2_DATABASE = None
        self.NMJv2_DBLOC = None
        self.USE_SYNOLOGYNOTIFIER = False
        self.SYNOLOGYNOTIFIER_NOTIFY_ONSNATCH = False
        self.SYNOLOGYNOTIFIER_NOTIFY_ONDOWNLOAD = False
        self.SYNOLOGYNOTIFIER_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.USE_TRAKT = False
        self.TRAKT_USERNAME = None
        self.TRAKT_ACCESS_TOKEN = None
        self.TRAKT_REFRESH_TOKEN = None
        self.TRAKT_REMOVE_WATCHLIST = False
        self.TRAKT_REMOVE_SERIESLIST = False
        self.TRAKT_REMOVE_SHOW_FROM_SICKRAGE = False
        self.TRAKT_SYNC_WATCHLIST = False
        self.TRAKT_METHOD_ADD = None
        self.TRAKT_START_PAUSED = False
        self.TRAKT_USE_RECOMMENDED = False
        self.TRAKT_SYNC = False
        self.TRAKT_SYNC_REMOVE = False
        self.TRAKT_DEFAULT_INDEXER = None
        self.TRAKT_TIMEOUT = None
        self.TRAKT_BLACKLIST_NAME = None
        self.USE_PYTIVO = False
        self.PYTIVO_NOTIFY_ONSNATCH = False
        self.PYTIVO_NOTIFY_ONDOWNLOAD = False
        self.PYTIVO_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.PYTIVO_UPDATE_LIBRARY = False
        self.PYTIVO_HOST = None
        self.PYTIVO_SHARE_NAME = None
        self.PYTIVO_TIVO_NAME = None
        self.USE_NMA = False
        self.NMA_NOTIFY_ONSNATCH = False
        self.NMA_NOTIFY_ONDOWNLOAD = False
        self.NMA_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.NMA_API = None
        self.NMA_PRIORITY = False
        self.USE_PUSHALOT = False
        self.PUSHALOT_NOTIFY_ONSNATCH = False
        self.PUSHALOT_NOTIFY_ONDOWNLOAD = False
        self.PUSHALOT_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.PUSHALOT_AUTHORIZATIONTOKEN = None
        self.USE_PUSHBULLET = False
        self.PUSHBULLET_NOTIFY_ONSNATCH = False
        self.PUSHBULLET_NOTIFY_ONDOWNLOAD = False
        self.PUSHBULLET_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.PUSHBULLET_API = None
        self.PUSHBULLET_DEVICE = None
        self.USE_EMAIL = False
        self.EMAIL_NOTIFY_ONSNATCH = False
        self.EMAIL_NOTIFY_ONDOWNLOAD = False
        self.EMAIL_NOTIFY_ONSUBTITLEDOWNLOAD = False
        self.EMAIL_HOST = None
        self.EMAIL_PORT = 25
        self.EMAIL_TLS = False
        self.EMAIL_USER = None
        self.EMAIL_PASSWORD = None
        self.EMAIL_FROM = None
        self.EMAIL_LIST = None
        self.GUI_NAME = None
        self.GUI_DIR = None
        self.HOME_LAYOUT = None
        self.HISTORY_LAYOUT = None
        self.HISTORY_LIMIT = 0
        self.DISPLAY_SHOW_SPECIALS = False
        self.COMING_EPS_LAYOUT = None
        self.COMING_EPS_DISPLAY_PAUSED = False
        self.COMING_EPS_SORT = None
        self.COMING_EPS_MISSED_RANGE = None
        self.FUZZY_DATING = False
        self.TRIM_ZERO = False
        self.DATE_PRESET = None
        self.TIME_PRESET = None
        self.TIME_PRESET_W_SECONDS = None
        self.TIMEZONE_DISPLAY = None
        self.THEME_NAME = None
        self.POSTER_SORTBY = None
        self.POSTER_SORTDIR = None
        self.FILTER_ROW = True
        self.USE_SUBTITLES = False
        self.SUBTITLES_LANGUAGES = None
        self.SUBTITLES_DIR = None
        self.SUBTITLES_SERVICES_LIST = None
        self.SUBTITLES_SERVICES_ENABLED = None
        self.SUBTITLES_HISTORY = False
        self.EMBEDDED_SUBTITLES_ALL = False
        self.SUBTITLES_HEARING_IMPAIRED = False
        self.SUBTITLES_MULTI = False
        self.SUBTITLES_EXTRA_SCRIPTS = None
        self.ADDIC7ED_USER = None
        self.ADDIC7ED_PASS = None
        self.OPENSUBTITLES_USER = None
        self.OPENSUBTITLES_PASS = None
        self.LEGENDASTV_USER = None
        self.LEGENDASTV_PASS = None
        self.ITASA_USER = None
        self.ITASA_PASS = None
        self.USE_FAILED_DOWNLOADS = False
        self.DELETE_FAILED = False
        self.EXTRA_SCRIPTS = None
        self.REQUIRE_WORDS = None
        self.IGNORE_WORDS = None
        self.IGNORED_SUBS_LIST = None
        self.SYNC_FILES = None
        self.CALENDAR_UNPROTECTED = False
        self.CALENDAR_ICONS = False
        self.NO_RESTART = False
        self.THETVDB_APITOKEN = None
        self.TRAKT_API_KEY = '5c65f55e11d48c35385d9e8670615763a605fad28374c8ae553a7b7a50651ddd'
        self.TRAKT_API_SECRET = 'b53e32045ac122a445ef163e6d859403301ffe9b17fb8321d428531b69022a82'
        self.TRAKT_PIN_URL = 'https://trakt.tv/pin/4562'
        self.TRAKT_OAUTH_URL = 'https://trakt.tv/'
        self.TRAKT_API_URL = 'https://api-v2launch.trakt.tv/'
        self.FANART_API_KEY = '9b3afaf26f6241bdb57d6cc6bd798da7'
        self.SHOWS_RECENT = []

        self.DEFAULT_AUTOPOSTPROCESSOR_FREQ = 10
        self.AUTOPOSTPROCESSOR_FREQ = None

        self.DEFAULT_NAMECACHE_FREQ = 10
        self.NAMECACHE_FREQ = None

        self.DEFAULT_DAILY_SEARCHER_FREQ = 40
        self.DAILY_SEARCHER_FREQ = None

        self.DEFAULT_BACKLOG_SEARCHER_FREQ = 21
        self.BACKLOG_SEARCHER_FREQ = None

        self.DEFAULT_VERSION_UPDATE_FREQ = 1
        self.VERSION_UPDATER_FREQ = None

        self.DEFAULT_SUBTITLE_SEARCHER_FREQ = 1
        self.SUBTITLE_SEARCHER_FREQ = None

        self.DEFAULT_SHOWUPDATE_HOUR = 3
        self.SHOWUPDATE_HOUR = None

        self.QUALITY_SIZES = {}

        self.CUSTOM_PROVIDERS = None

        self.GIT_REMOTE = "origin"
        self.GIT_REMOTE_URL = "https://git.sickrage.ca/SiCKRAGE/sickrage"

        self.RANDOM_USER_AGENT = False

    def change_https_cert(self, https_cert):
        """
        Replace HTTPS Certificate file path
    
        :param https_cert: path to the new certificate file
        :return: True on success, False on failure
        """

        if https_cert == '':
            self.HTTPS_CERT = ''
            return True

        if os.path.normpath(self.HTTPS_CERT) != os.path.normpath(https_cert):
            if makeDir(os.path.dirname(os.path.abspath(https_cert))):
                self.HTTPS_CERT = os.path.normpath(https_cert)
                sickrage.srCore.srLogger.info("Changed https cert path to " + https_cert)
            else:
                return False

        return True

    def change_https_key(self, https_key):
        """
        Replace HTTPS Key file path
    
        :param https_key: path to the new key file
        :return: True on success, False on failure
        """
        if https_key == '':
            self.HTTPS_KEY = ''
            return True

        if os.path.normpath(self.HTTPS_KEY) != os.path.normpath(https_key):
            if makeDir(os.path.dirname(os.path.abspath(https_key))):
                self.HTTPS_KEY = os.path.normpath(https_key)
                sickrage.srCore.srLogger.info("Changed https key path to " + https_key)
            else:
                return False

        return True

    def change_nzb_dir(self, nzb_dir):
        """
        Change NZB Folder
    
        :param nzb_dir: New NZB Folder location
        :return: True on success, False on failure
        """
        if nzb_dir == '':
            self.NZB_DIR = ''
            return True

        if os.path.normpath(self.NZB_DIR) != os.path.normpath(nzb_dir):
            if makeDir(nzb_dir):
                self.NZB_DIR = os.path.normpath(nzb_dir)
                sickrage.srCore.srLogger.info("Changed NZB folder to " + nzb_dir)
            else:
                return False

        return True

    def change_torrent_dir(self, torrent_dir):
        """
        Change torrent directory
    
        :param torrent_dir: New torrent directory
        :return: True on success, False on failure
        """
        if torrent_dir == '':
            self.TORRENT_DIR = ''
            return True

        if os.path.normpath(self.TORRENT_DIR) != os.path.normpath(torrent_dir):
            if makeDir(torrent_dir):
                self.TORRENT_DIR = os.path.normpath(torrent_dir)
                sickrage.srCore.srLogger.info("Changed torrent folder to " + torrent_dir)
            else:
                return False

        return True

    def change_tv_download_dir(self, tv_download_dir):
        """
        Change TV_DOWNLOAD directory (used by postprocessor)
    
        :param tv_download_dir: New tv download directory
        :return: True on success, False on failure
        """
        if tv_download_dir == '':
            self.TV_DOWNLOAD_DIR = ''
            return True

        if os.path.normpath(self.TV_DOWNLOAD_DIR) != os.path.normpath(tv_download_dir):
            if makeDir(tv_download_dir):
                self.TV_DOWNLOAD_DIR = os.path.normpath(tv_download_dir)
                sickrage.srCore.srLogger.info("Changed TV download folder to " + tv_download_dir)
            else:
                return False

        return True

    def change_autopostprocessor_freq(self, freq):
        """
        Change frequency of automatic postprocessing thread
        TODO: Make all thread frequency changers in config.py return True/False status
    
        :param freq: New frequency
        """
        self.AUTOPOSTPROCESSOR_FREQ = self.to_int(freq, default=self.DEFAULT_AUTOPOSTPROCESSOR_FREQ)

        if self.AUTOPOSTPROCESSOR_FREQ < self.MIN_AUTOPOSTPROCESSOR_FREQ:
            self.AUTOPOSTPROCESSOR_FREQ = self.MIN_AUTOPOSTPROCESSOR_FREQ

        sickrage.srCore.srScheduler.modify_job('POSTPROCESSOR',
                                               trigger=srIntervalTrigger(
                                                   **{'minutes': self.AUTOPOSTPROCESSOR_FREQ,
                                                      'min': self.MIN_AUTOPOSTPROCESSOR_FREQ}))

    def change_daily_searcher_freq(self, freq):
        """
        Change frequency of daily search thread
    
        :param freq: New frequency
        """
        self.DAILY_SEARCHER_FREQ = self.to_int(freq, default=self.DEFAULT_DAILY_SEARCHER_FREQ)
        sickrage.srCore.srScheduler.modify_job('DAILYSEARCHER',
                                               trigger=srIntervalTrigger(
                                                   **{'minutes': self.DAILY_SEARCHER_FREQ,
                                                      'min': self.MIN_DAILY_SEARCHER_FREQ}))

    def change_backlog_searcher_freq(self, freq):
        """
        Change frequency of backlog thread
    
        :param freq: New frequency
        """
        self.BACKLOG_SEARCHER_FREQ = self.to_int(freq, default=self.DEFAULT_BACKLOG_SEARCHER_FREQ)
        self.MIN_BACKLOG_SEARCHER_FREQ = sickrage.srCore.BACKLOGSEARCHER.get_backlog_cycle_time()
        sickrage.srCore.srScheduler.modify_job('BACKLOG',
                                               trigger=srIntervalTrigger(
                                                   **{'minutes': self.BACKLOG_SEARCHER_FREQ,
                                                      'min': self.MIN_BACKLOG_SEARCHER_FREQ}))

    def change_updater_freq(self, freq):
        """
        Change frequency of version updater thread
    
        :param freq: New frequency
        """
        self.VERSION_UPDATER_FREQ = self.to_int(freq, default=self.DEFAULT_VERSION_UPDATE_FREQ)
        sickrage.srCore.srScheduler.modify_job('VERSIONUPDATER',
                                               trigger=srIntervalTrigger(
                                                   **{'hours': self.VERSION_UPDATER_FREQ,
                                                      'min': self.MIN_VERSION_UPDATER_FREQ}))

    def change_showupdate_hour(self, freq):
        """
        Change frequency of show updater thread
    
        :param freq: New frequency
        """
        self.SHOWUPDATE_HOUR = self.to_int(freq, default=self.DEFAULT_SHOWUPDATE_HOUR)
        if self.SHOWUPDATE_HOUR < 0 or self.SHOWUPDATE_HOUR > 23:
            self.SHOWUPDATE_HOUR = 0

        sickrage.srCore.srScheduler.modify_job('SHOWUPDATER',
                                               trigger=srIntervalTrigger(
                                                   **{'hours': 1,
                                                      'start_date': datetime.datetime.now().replace(
                                                          hour=self.SHOWUPDATE_HOUR)}))

    def change_subtitle_searcher_freq(self, freq):
        """
        Change frequency of subtitle thread
    
        :param freq: New frequency
        """
        self.SUBTITLE_SEARCHER_FREQ = self.to_int(freq, default=self.DEFAULT_SUBTITLE_SEARCHER_FREQ)
        sickrage.srCore.srScheduler.modify_job('SUBTITLESEARCHER',
                                               trigger=srIntervalTrigger(
                                                   **{'hours': self.SUBTITLE_SEARCHER_FREQ,
                                                      'min': self.MIN_SUBTITLE_SEARCHER_FREQ}))

    def change_version_notify(self, version_notify):
        """
        Change frequency of versioncheck thread
    
        :param version_notify: New frequency
        """
        self.VERSION_NOTIFY = self.checkbox_to_value(version_notify)
        if not self.VERSION_NOTIFY:
            sickrage.srCore.NEWEST_VERSION_STRING = None

    def change_download_propers(self, download_propers):
        """
        Enable/Disable proper download thread
        TODO: Make this return True/False on success/failure
    
        :param download_propers: New desired state
        """
        self.DOWNLOAD_PROPERS = self.checkbox_to_value(download_propers)
        job = sickrage.srCore.srScheduler.get_job('PROPERSEARCHER')
        (job.pause, job.resume)[self.DOWNLOAD_PROPERS]()

    def change_use_trakt(self, use_trakt):
        """
        Enable/disable trakt thread
        TODO: Make this return true/false on success/failure
    
        :param use_trakt: New desired state
        """
        self.USE_TRAKT = self.checkbox_to_value(use_trakt)
        job = sickrage.srCore.srScheduler.get_job('TRAKTSEARCHER')
        (job.pause, job.resume)[self.USE_TRAKT]()

    def change_use_subtitles(self, use_subtitles):
        """
        Enable/Disable subtitle searcher
        TODO: Make this return true/false on success/failure
    
        :param use_subtitles: New desired state
        """
        self.USE_SUBTITLES = self.checkbox_to_value(use_subtitles)
        job = sickrage.srCore.srScheduler.get_job('SUBTITLESEARCHER')
        (job.pause, job.resume)[self.USE_SUBTITLES]()

    def change_process_automatically(self, process_automatically):
        """
        Enable/Disable postprocessor thread
        TODO: Make this return True/False on success/failure
    
        :param process_automatically: New desired state
        """
        self.PROCESS_AUTOMATICALLY = self.checkbox_to_value(process_automatically)
        job = sickrage.srCore.srScheduler.get_job('POSTPROCESSOR')
        (job.pause, job.resume)[self.PROCESS_AUTOMATICALLY]()

    def checkbox_to_value(self, option, value_on=1, value_off=0):
        """
        Turns checkbox option 'on' or 'true' to value_on (1)
        any other value returns value_off (0)
        """

        if isinstance(option, list):
            option = option[-1]

        if option == 'on' or option == 'true':
            return value_on

        return value_off

    def clean_host(self, host, default_port=None):
        """
        Returns host or host:port or empty string from a given url or host
        If no port is found and default_port is given use host:default_port
        """

        host = host.strip()

        if host:

            match_host_port = re.search(r'(?:http.*://)?(?P<host>[^:/]+).?(?P<port>[0-9]*).*', host)

            cleaned_host = match_host_port.group('host')
            cleaned_port = match_host_port.group('port')

            if cleaned_host:

                if cleaned_port:
                    host = cleaned_host + ':' + cleaned_port

                elif default_port:
                    host = cleaned_host + ':' + str(default_port)

                else:
                    host = cleaned_host

            else:
                host = ''

        return host

    def clean_hosts(self, hosts, default_port=None):
        """
        Returns list of cleaned hosts by Config.clean_host
    
        :param hosts: list of hosts
        :param default_port: default port to use
        :return: list of cleaned hosts
        """
        cleaned_hosts = []

        for cur_host in [x.strip() for x in hosts.split(",")]:
            if cur_host:
                cleaned_host = self.clean_host(cur_host, default_port)
                if cleaned_host:
                    cleaned_hosts.append(cleaned_host)

        if cleaned_hosts:
            cleaned_hosts = ",".join(cleaned_hosts)

        else:
            cleaned_hosts = ''

        return cleaned_hosts

    def to_int(self, val, default=0):
        """ Return int value of val or default on error """

        try:
            val = int(val)
        except Exception:
            val = default

        return val

    ################################################################################
    # Check_setting_int                                                            #
    ################################################################################

    def minimax(self, val, default, low, high):
        """ Return value forced within range """

        val = self.to_int(val, default=default)

        if val < low:
            return low
        if val > high:
            return high

        return val

    ################################################################################
    # Check_setting_int                                                            #
    ################################################################################

    def check_setting_int(self, section, key, def_val, silent=True):
        my_val = self.CONFIG_OBJ.get(section, {section: key}).get(key, def_val)
        if str(my_val).lower() == "true":
            my_val = 1
        elif str(my_val).lower() == "false":
            my_val = 0

        try:
            my_val = int(my_val)
        except Exception:
            my_val = def_val

        if not silent:
            sickrage.srCore.srLogger.debug(key + " -> " + str(my_val))

        return my_val

    ################################################################################
    # Check_setting_float                                                          #
    ################################################################################

    def check_setting_float(self, section, key, def_val, silent=True):
        try:
            my_val = float(self.CONFIG_OBJ.get(section, {section: key}).get(key, def_val))
        except Exception:
            my_val = def_val

        if not silent:
            sickrage.srCore.srLogger.debug(section + " -> " + str(my_val))

        return my_val

    ################################################################################
    # Check_setting_str                                                            #
    ################################################################################
    def check_setting_str(self, section, key, def_val="", silent=True):
        my_val = self.CONFIG_OBJ.get(section, {section: key}).get(key, def_val)

        if my_val:
            censored_regex = re.compile(r"|".join(re.escape(word) for word in ["password", "token", "api"]), re.I)
            if censored_regex.search(key) or (section, key) in self.CENSORED_ITEMS:
                self.CENSORED_ITEMS[section, key] = my_val

        if not silent:
            print(key + " -> " + my_val)

        return my_val

    ################################################################################
    # Check_setting_pickle                                                           #
    ################################################################################
    def check_setting_pickle(self, section, key, def_val="", silent=True):
        my_val = pickle.loads(self.CONFIG_OBJ.get(section, {section: key}).get(key, pickle.dumps(def_val)))

        if not silent:
            print(key + " -> " + my_val)

        return my_val

    def load(self):
        # Make sure we can write to the config file
        if not os.path.isabs(sickrage.CONFIG_FILE):
            sickrage.CONFIG_FILE = os.path.abspath(os.path.join(sickrage.DATA_DIR, sickrage.CONFIG_FILE))

        if not os.access(sickrage.CONFIG_FILE, os.W_OK):
            if os.path.isfile(sickrage.CONFIG_FILE):
                raise SystemExit("Config file '" + sickrage.CONFIG_FILE + "' must be writeable.")
            elif not os.access(os.path.dirname(sickrage.CONFIG_FILE), os.W_OK):
                raise SystemExit(
                    "Config file root dir '" + os.path.dirname(sickrage.CONFIG_FILE) + "' must be writeable.")

        # load config
        self.CONFIG_OBJ = ConfigObj(sickrage.CONFIG_FILE)

        # decrypt settings
        self.ENCRYPTION_VERSION = self.check_setting_int('General', 'encryption_version', 0)
        self.ENCRYPTION_SECRET = self.check_setting_str('General', 'encryption_secret', generateCookieSecret())
        self.CONFIG_OBJ.walk(self.decrypt)

        # migrate config
        self.CONFIG_OBJ = ConfigMigrator(self.CONFIG_OBJ).migrate_config()

        sickrage.DEBUG = sickrage.DEBUG or bool(self.check_setting_int('General', 'debug', 0))
        sickrage.DEVELOPER = sickrage.DEVELOPER or bool(self.check_setting_int('General', 'developer', 0))

        # last database compact
        self.LAST_DB_COMPACT = self.check_setting_int('General', 'last_db_compact', 0)

        # logging settings
        self.LOG_NR = self.check_setting_int('General', 'log_nr', 5)
        self.LOG_SIZE = self.check_setting_int('General', 'log_size', 1048576)
        self.LOG_DIR = os.path.abspath(os.path.join(sickrage.DATA_DIR, 'logs'))
        self.LOG_FILE = os.path.abspath(os.path.join(self.LOG_DIR, 'sickrage.log'))

        # misc settings
        self.GUI_NAME = self.check_setting_str('GUI', 'gui_name', 'default')
        self.GUI_DIR = os.path.join(sickrage.PROG_DIR, 'core', 'webserver', 'gui', self.GUI_NAME)
        self.THEME_NAME = self.check_setting_str('GUI', 'theme_name', 'dark')
        self.SOCKET_TIMEOUT = self.check_setting_int('General', 'socket_timeout', 30)

        self.DEFAULT_PAGE = self.check_setting_str('General', 'default_page', 'home')

        self.PIP_PATH = self.check_setting_str('General', 'pip_path', 'pip')

        self.GIT_PATH = self.check_setting_str('General', 'git_path', 'git')
        self.GIT_AUTOISSUES = bool(self.check_setting_int('General', 'git_autoissues', 0))
        self.GIT_USERNAME = self.check_setting_str('General', 'git_username', '')
        self.GIT_PASSWORD = self.check_setting_str('General', 'git_password', '')
        self.GIT_NEWVER = bool(self.check_setting_int('General', 'git_newver', 0))
        self.GIT_RESET = bool(self.check_setting_int('General', 'git_reset', 1))

        # web settings
        self.WEB_PORT = self.check_setting_int('General', 'web_port', 8081)
        if sickrage.WEB_PORT != 8081:
            self.WEB_PORT = sickrage.WEB_PORT

        self.WEB_HOST = self.check_setting_str('General', 'web_host', get_lan_ip())
        self.WEB_IPV6 = bool(self.check_setting_int('General', 'web_ipv6', 0))
        self.WEB_ROOT = self.check_setting_str('General', 'web_root', '').rstrip("/")
        self.WEB_LOG = bool(self.check_setting_int('General', 'web_log', 0))
        self.WEB_USERNAME = self.check_setting_str('General', 'web_username', '')
        self.WEB_PASSWORD = self.check_setting_str('General', 'web_password', '')
        self.WEB_COOKIE_SECRET = self.check_setting_str(
            'General', 'web_cookie_secret', generateCookieSecret()
        )
        self.WEB_USE_GZIP = bool(self.check_setting_int('General', 'web_use_gzip', 1))

        self.SSL_VERIFY = bool(self.check_setting_int('General', 'ssl_verify', 1))
        self.LAUNCH_BROWSER = bool(self.check_setting_int('General', 'launch_browser', 1))
        self.INDEXER_DEFAULT_LANGUAGE = self.check_setting_str('General', 'indexerDefaultLang', 'en')
        self.EP_DEFAULT_DELETED_STATUS = self.check_setting_int('General', 'ep_default_deleted_status',
                                                                6)
        self.DOWNLOAD_URL = self.check_setting_str('General', 'download_url', "")
        self.CPU_PRESET = self.check_setting_str('General', 'cpu_preset', 'NORMAL')
        self.ANON_REDIRECT = self.check_setting_str('General', 'anon_redirect',
                                                    'http://nullrefer.com/?')
        self.PROXY_SETTING = self.check_setting_str('General', 'proxy_setting', '')
        self.PROXY_INDEXERS = bool(self.check_setting_int('General', 'proxy_indexers', 1))
        self.TRASH_REMOVE_SHOW = bool(self.check_setting_int('General', 'trash_remove_show', 0))
        self.TRASH_ROTATE_LOGS = bool(self.check_setting_int('General', 'trash_rotate_logs', 0))
        self.SORT_ARTICLE = bool(self.check_setting_int('General', 'sort_article', 0))
        self.API_KEY = self.check_setting_str('General', 'api_key', '')

        if not self.ENABLE_HTTPS:
            self.ENABLE_HTTPS = bool(self.check_setting_int('General', 'enable_https', 0))

        self.HTTPS_CERT = os.path.abspath(
            os.path.join(sickrage.PROG_DIR, self.check_setting_str('General', 'https_cert', 'server.crt')))
        self.HTTPS_KEY = os.path.abspath(
            os.path.join(sickrage.PROG_DIR, self.check_setting_str('General', 'https_key', 'server.key')))

        self.HANDLE_REVERSE_PROXY = bool(self.check_setting_int('General', 'handle_reverse_proxy', 0))

        # show settings
        self.ROOT_DIRS = self.check_setting_str('General', 'root_dirs', '')
        self.QUALITY_DEFAULT = self.check_setting_int('General', 'quality_default', SD)
        self.STATUS_DEFAULT = self.check_setting_int('General', 'status_default', SKIPPED)
        self.STATUS_DEFAULT_AFTER = self.check_setting_int('General', 'status_default_after', WANTED)
        self.VERSION_NOTIFY = bool(self.check_setting_int('General', 'version_notify', 1))
        self.AUTO_UPDATE = bool(self.check_setting_int('General', 'auto_update', 0))
        self.NOTIFY_ON_UPDATE = bool(self.check_setting_int('General', 'notify_on_update', 1))
        self.FLATTEN_FOLDERS_DEFAULT = bool(
            self.check_setting_int('General', 'flatten_folders_default', 0))
        self.INDEXER_DEFAULT = self.check_setting_int('General', 'indexer_default', 0)
        self.INDEXER_TIMEOUT = self.check_setting_int('General', 'indexer_timeout', 120)
        self.ANIME_DEFAULT = bool(self.check_setting_int('General', 'anime_default', 0))
        self.SCENE_DEFAULT = bool(self.check_setting_int('General', 'scene_default', 0))
        self.ARCHIVE_DEFAULT = bool(self.check_setting_int('General', 'archive_default', 0))

        # naming settings
        self.NAMING_PATTERN = self.check_setting_str('General', 'naming_pattern',
                                                     'Season %0S/%SN - S%0SE%0E - %EN')
        self.NAMING_ABD_PATTERN = self.check_setting_str('General', 'naming_abd_pattern',
                                                         '%SN - %A.D - %EN')
        self.NAMING_CUSTOM_ABD = bool(self.check_setting_int('General', 'naming_custom_abd', 0))
        self.NAMING_SPORTS_PATTERN = self.check_setting_str('General', 'naming_sports_pattern',
                                                            '%SN - %A-D - %EN')
        self.NAMING_ANIME_PATTERN = self.check_setting_str('General', 'naming_anime_pattern',
                                                           'Season %0S/%SN - S%0SE%0E - %EN')
        self.NAMING_ANIME = self.check_setting_int('General', 'naming_anime', 3)
        self.NAMING_CUSTOM_SPORTS = bool(self.check_setting_int('General', 'naming_custom_sports', 0))
        self.NAMING_CUSTOM_ANIME = bool(self.check_setting_int('General', 'naming_custom_anime', 0))
        self.NAMING_MULTI_EP = self.check_setting_int('General', 'naming_multi_ep', 1)
        self.NAMING_ANIME_MULTI_EP = self.check_setting_int('General', 'naming_anime_multi_ep', 1)
        self.NAMING_STRIP_YEAR = bool(self.check_setting_int('General', 'naming_strip_year', 0))

        # provider settings
        self.USE_NZBS = bool(self.check_setting_int('General', 'use_nzbs', 0))
        self.USE_TORRENTS = bool(self.check_setting_int('General', 'use_torrents', 1))
        self.NZB_METHOD = self.check_setting_str('General', 'nzb_method', 'blackhole')
        self.TORRENT_METHOD = self.check_setting_str('General', 'torrent_method', 'blackhole')
        self.DOWNLOAD_PROPERS = bool(self.check_setting_int('General', 'download_propers', 1))
        self.ENABLE_RSS_CACHE = bool(self.check_setting_int('General', 'enable_rss_cache', 1))
        self.PROPER_SEARCHER_INTERVAL = self.check_setting_str('General', 'check_propers_interval',
                                                               'daily')
        self.RANDOMIZE_PROVIDERS = bool(self.check_setting_int('General', 'randomize_providers', 0))
        self.ALLOW_HIGH_PRIORITY = bool(self.check_setting_int('General', 'allow_high_priority', 1))
        self.SKIP_REMOVED_FILES = bool(self.check_setting_int('General', 'skip_removed_files', 0))
        self.USENET_RETENTION = self.check_setting_int('General', 'usenet_retention', 500)

        # SCHEDULER.settings
        self.AUTOPOSTPROCESSOR_FREQ = self.check_setting_int(
            'General', 'autopostprocessor_frequency', self.DEFAULT_AUTOPOSTPROCESSOR_FREQ
        )

        self.SUBTITLE_SEARCHER_FREQ = self.check_setting_int(
            'Subtitles', 'subtitles_finder_frequency', self.DEFAULT_SUBTITLE_SEARCHER_FREQ
        )

        self.NAMECACHE_FREQ = self.check_setting_int('General', 'namecache_frequency',
                                                     self.DEFAULT_NAMECACHE_FREQ)
        self.DAILY_SEARCHER_FREQ = self.check_setting_int('General', 'dailysearch_frequency',
                                                          self.DEFAULT_DAILY_SEARCHER_FREQ)
        self.BACKLOG_SEARCHER_FREQ = self.check_setting_int('General', 'backlog_frequency',
                                                            self.DEFAULT_BACKLOG_SEARCHER_FREQ)
        self.VERSION_UPDATER_FREQ = self.check_setting_int('General', 'update_frequency',
                                                           self.DEFAULT_VERSION_UPDATE_FREQ)
        self.SHOWUPDATE_STALE = bool(self.check_setting_int('General', 'showupdate_stale', 1))
        self.SHOWUPDATE_HOUR = self.check_setting_int('General', 'showupdate_hour',
                                                      self.DEFAULT_SHOWUPDATE_HOUR)
        self.BACKLOG_DAYS = self.check_setting_int('General', 'backlog_days', 7)

        self.NZB_DIR = self.check_setting_str('Blackhole', 'nzb_dir', '')
        self.TORRENT_DIR = self.check_setting_str('Blackhole', 'torrent_dir', '')

        self.TV_DOWNLOAD_DIR = self.check_setting_str('General', 'tv_download_dir', '')
        self.PROCESS_AUTOMATICALLY = bool(self.check_setting_int('General', 'process_automatically', 0))
        self.NO_DELETE = bool(self.check_setting_int('General', 'no_delete', 0))
        self.UNPACK = bool(self.check_setting_int('General', 'unpack', 0))
        self.RENAME_EPISODES = bool(self.check_setting_int('General', 'rename_episodes', 1))
        self.AIRDATE_EPISODES = bool(self.check_setting_int('General', 'airdate_episodes', 0))
        self.FILE_TIMESTAMP_TIMEZONE = self.check_setting_str('General', 'file_timestamp_timezone',
                                                              'network')
        self.KEEP_PROCESSED_DIR = bool(self.check_setting_int('General', 'keep_processed_dir', 1))
        self.PROCESS_METHOD = self.check_setting_str('General', 'process_method',
                                                     'copy' if self.KEEP_PROCESSED_DIR else'move')
        self.DELRARCONTENTS = bool(self.check_setting_int('General', 'del_rar_contents', 0))
        self.MOVE_ASSOCIATED_FILES = bool(self.check_setting_int('General', 'move_associated_files', 0))
        self.POSTPONE_IF_SYNC_FILES = bool(
            self.check_setting_int('General', 'postpone_if_sync_files', 1))
        self.SYNC_FILES = self.check_setting_str('General', 'sync_files',
                                                 '!sync,lftp-pget-status,part,bts,!qb')
        self.NFO_RENAME = bool(self.check_setting_int('General', 'nfo_rename', 1))
        self.CREATE_MISSING_SHOW_DIRS = bool(
            self.check_setting_int('General', 'create_missing_show_dirs', 0))
        self.ADD_SHOWS_WO_DIR = bool(self.check_setting_int('General', 'add_shows_wo_dir', 0))

        self.NZBS = bool(self.check_setting_int('NZBs', 'nzbs', 0))
        self.NZBS_UID = self.check_setting_str('NZBs', 'nzbs_uid', '')
        self.NZBS_HASH = self.check_setting_str('NZBs', 'nzbs_hash', '')

        self.NEWZBIN = bool(self.check_setting_int('Newzbin', 'newzbin', 0))
        self.NEWZBIN_USERNAME = self.check_setting_str('Newzbin', 'newzbin_username', '')
        self.NEWZBIN_PASSWORD = self.check_setting_str('Newzbin', 'newzbin_password', '')

        self.SAB_USERNAME = self.check_setting_str('SABnzbd', 'sab_username', '')
        self.SAB_PASSWORD = self.check_setting_str('SABnzbd', 'sab_password', '')
        self.SAB_APIKEY = self.check_setting_str('SABnzbd', 'sab_apikey', '')
        self.SAB_CATEGORY = self.check_setting_str('SABnzbd', 'sab_category', 'tv')
        self.SAB_CATEGORY_BACKLOG = self.check_setting_str('SABnzbd', 'sab_category_backlog',
                                                           self.SAB_CATEGORY)
        self.SAB_CATEGORY_ANIME = self.check_setting_str('SABnzbd', 'sab_category_anime', 'anime')
        self.SAB_CATEGORY_ANIME_BACKLOG = self.check_setting_str('SABnzbd',
                                                                 'sab_category_anime_backlog',
                                                                 self.SAB_CATEGORY_ANIME)
        self.SAB_HOST = self.check_setting_str('SABnzbd', 'sab_host', '')
        self.SAB_FORCED = bool(self.check_setting_int('SABnzbd', 'sab_forced', 0))

        self.NZBGET_USERNAME = self.check_setting_str('NZBget', 'nzbget_username', 'nzbget')
        self.NZBGET_PASSWORD = self.check_setting_str('NZBget', 'nzbget_password', 'tegbzn6789')
        self.NZBGET_CATEGORY = self.check_setting_str('NZBget', 'nzbget_category', 'tv')
        self.NZBGET_CATEGORY_BACKLOG = self.check_setting_str('NZBget', 'nzbget_category_backlog',
                                                              self.NZBGET_CATEGORY)
        self.NZBGET_CATEGORY_ANIME = self.check_setting_str('NZBget', 'nzbget_category_anime', 'anime')
        self.NZBGET_CATEGORY_ANIME_BACKLOG = self.check_setting_str(
            'NZBget', 'nzbget_category_anime_backlog', self.NZBGET_CATEGORY_ANIME)
        self.NZBGET_HOST = self.check_setting_str('NZBget', 'nzbget_host', '')
        self.NZBGET_USE_HTTPS = bool(self.check_setting_int('NZBget', 'nzbget_use_https', 0))
        self.NZBGET_PRIORITY = self.check_setting_int('NZBget', 'nzbget_priority', 100)

        self.TORRENT_USERNAME = self.check_setting_str('TORRENT', 'torrent_username', '')
        self.TORRENT_PASSWORD = self.check_setting_str('TORRENT', 'torrent_password', '')
        self.TORRENT_HOST = self.check_setting_str('TORRENT', 'torrent_host', '')
        self.TORRENT_PATH = self.check_setting_str('TORRENT', 'torrent_path', '')
        self.TORRENT_SEED_TIME = self.check_setting_int('TORRENT', 'torrent_seed_time', 0)
        self.TORRENT_PAUSED = bool(self.check_setting_int('TORRENT', 'torrent_paused', 0))
        self.TORRENT_HIGH_BANDWIDTH = bool(
            self.check_setting_int('TORRENT', 'torrent_high_bandwidth', 0))
        self.TORRENT_LABEL = self.check_setting_str('TORRENT', 'torrent_label', '')
        self.TORRENT_LABEL_ANIME = self.check_setting_str('TORRENT', 'torrent_label_anime', '')
        self.TORRENT_VERIFY_CERT = bool(self.check_setting_int('TORRENT', 'torrent_verify_cert', 0))
        self.TORRENT_RPCURL = self.check_setting_str('TORRENT', 'torrent_rpcurl', 'transmission')
        self.TORRENT_AUTH_TYPE = self.check_setting_str('TORRENT', 'torrent_auth_type', '')
        self.TORRENT_TRACKERS = self.check_setting_str('TORRENT', 'torrent_trackers', self.TORRENT_TRACKERS)

        self.USE_KODI = bool(self.check_setting_int('KODI', 'use_kodi', 0))
        self.KODI_ALWAYS_ON = bool(self.check_setting_int('KODI', 'kodi_always_on', 1))
        self.KODI_NOTIFY_ONSNATCH = bool(self.check_setting_int('KODI', 'kodi_notify_onsnatch', 0))
        self.KODI_NOTIFY_ONDOWNLOAD = bool(self.check_setting_int('KODI', 'kodi_notify_ondownload', 0))
        self.KODI_NOTIFY_ONSUBTITLEDOWNLOAD = bool(self.check_setting_int('KODI', 'kodi_notify_onsubtitledownload', 0))
        self.KODI_UPDATE_LIBRARY = bool(self.check_setting_int('KODI', 'kodi_update_library', 0))
        self.KODI_UPDATE_FULL = bool(self.check_setting_int('KODI', 'kodi_update_full', 0))
        self.KODI_UPDATE_ONLYFIRST = bool(self.check_setting_int('KODI', 'kodi_update_onlyfirst', 0))
        self.KODI_HOST = self.check_setting_str('KODI', 'kodi_host', '')
        self.KODI_USERNAME = self.check_setting_str('KODI', 'kodi_username', '')
        self.KODI_PASSWORD = self.check_setting_str('KODI', 'kodi_password', '')

        self.USE_PLEX = bool(self.check_setting_int('Plex', 'use_plex', 0))
        self.PLEX_NOTIFY_ONSNATCH = bool(self.check_setting_int('Plex', 'plex_notify_onsnatch', 0))
        self.PLEX_NOTIFY_ONDOWNLOAD = bool(self.check_setting_int('Plex', 'plex_notify_ondownload', 0))
        self.PLEX_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Plex', 'plex_notify_onsubtitledownload', 0))
        self.PLEX_UPDATE_LIBRARY = bool(self.check_setting_int('Plex', 'plex_update_library', 0))
        self.PLEX_SERVER_HOST = self.check_setting_str('Plex', 'plex_server_host', '')
        self.PLEX_SERVER_TOKEN = self.check_setting_str('Plex', 'plex_server_token', '')
        self.PLEX_HOST = self.check_setting_str('Plex', 'plex_host', '')
        self.PLEX_USERNAME = self.check_setting_str('Plex', 'plex_username', '')
        self.PLEX_PASSWORD = self.check_setting_str('Plex', 'plex_password', '')
        self.USE_PLEX_CLIENT = bool(self.check_setting_int('Plex', 'use_plex_client', 0))
        self.PLEX_CLIENT_USERNAME = self.check_setting_str('Plex', 'plex_client_username', '')
        self.PLEX_CLIENT_PASSWORD = self.check_setting_str('Plex', 'plex_client_password', '')

        self.USE_EMBY = bool(self.check_setting_int('Emby', 'use_emby', 0))
        self.EMBY_HOST = self.check_setting_str('Emby', 'emby_host', '')
        self.EMBY_APIKEY = self.check_setting_str('Emby', 'emby_apikey', '')

        self.USE_GROWL = bool(self.check_setting_int('Growl', 'use_growl', 0))
        self.GROWL_NOTIFY_ONSNATCH = bool(self.check_setting_int('Growl', 'growl_notify_onsnatch', 0))
        self.GROWL_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Growl', 'growl_notify_ondownload', 0))
        self.GROWL_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Growl', 'growl_notify_onsubtitledownload', 0))
        self.GROWL_HOST = self.check_setting_str('Growl', 'growl_host', '')
        self.GROWL_PASSWORD = self.check_setting_str('Growl', 'growl_password', '')

        self.USE_FREEMOBILE = bool(self.check_setting_int('FreeMobile', 'use_freemobile', 0))
        self.FREEMOBILE_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('FreeMobile', 'freemobile_notify_onsnatch', 0))
        self.FREEMOBILE_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('FreeMobile', 'freemobile_notify_ondownload', 0))
        self.FREEMOBILE_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('FreeMobile', 'freemobile_notify_onsubtitledownload', 0))
        self.FREEMOBILE_ID = self.check_setting_str('FreeMobile', 'freemobile_id', '')
        self.FREEMOBILE_APIKEY = self.check_setting_str('FreeMobile', 'freemobile_apikey', '')

        self.USE_PROWL = bool(self.check_setting_int('Prowl', 'use_prowl', 0))
        self.PROWL_NOTIFY_ONSNATCH = bool(self.check_setting_int('Prowl', 'prowl_notify_onsnatch', 0))
        self.PROWL_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Prowl', 'prowl_notify_ondownload', 0))
        self.PROWL_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Prowl', 'prowl_notify_onsubtitledownload', 0))
        self.PROWL_API = self.check_setting_str('Prowl', 'prowl_api', '')
        self.PROWL_PRIORITY = self.check_setting_str('Prowl', 'prowl_priority', "0")

        self.USE_TWITTER = bool(self.check_setting_int('Twitter', 'use_twitter', 0))
        self.TWITTER_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('Twitter', 'twitter_notify_onsnatch', 0))
        self.TWITTER_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Twitter', 'twitter_notify_ondownload', 0))
        self.TWITTER_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Twitter', 'twitter_notify_onsubtitledownload', 0))
        self.TWITTER_USERNAME = self.check_setting_str('Twitter', 'twitter_username', '')
        self.TWITTER_PASSWORD = self.check_setting_str('Twitter', 'twitter_password', '')
        self.TWITTER_PREFIX = self.check_setting_str('Twitter', 'twitter_prefix', 'SiCKRAGE')
        self.TWITTER_DMTO = self.check_setting_str('Twitter', 'twitter_dmto', '')
        self.TWITTER_USEDM = bool(self.check_setting_int('Twitter', 'twitter_usedm', 0))

        self.USE_BOXCAR = bool(self.check_setting_int('Boxcar', 'use_boxcar', 0))
        self.BOXCAR_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('Boxcar', 'boxcar_notify_onsnatch', 0))
        self.BOXCAR_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Boxcar', 'boxcar_notify_ondownload', 0))
        self.BOXCAR_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Boxcar', 'boxcar_notify_onsubtitledownload', 0))
        self.BOXCAR_USERNAME = self.check_setting_str('Boxcar', 'boxcar_username', '')

        self.USE_BOXCAR2 = bool(self.check_setting_int('Boxcar2', 'use_boxcar2', 0))
        self.BOXCAR2_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('Boxcar2', 'boxcar2_notify_onsnatch', 0))
        self.BOXCAR2_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Boxcar2', 'boxcar2_notify_ondownload', 0))
        self.BOXCAR2_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Boxcar2', 'boxcar2_notify_onsubtitledownload', 0))
        self.BOXCAR2_ACCESSTOKEN = self.check_setting_str('Boxcar2', 'boxcar2_accesstoken', '')

        self.USE_PUSHOVER = bool(self.check_setting_int('Pushover', 'use_pushover', 0))
        self.PUSHOVER_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('Pushover', 'pushover_notify_onsnatch', 0))
        self.PUSHOVER_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Pushover', 'pushover_notify_ondownload', 0))
        self.PUSHOVER_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Pushover', 'pushover_notify_onsubtitledownload', 0))
        self.PUSHOVER_USERKEY = self.check_setting_str('Pushover', 'pushover_userkey', '')
        self.PUSHOVER_APIKEY = self.check_setting_str('Pushover', 'pushover_apikey', '')
        self.PUSHOVER_DEVICE = self.check_setting_str('Pushover', 'pushover_device', '')
        self.PUSHOVER_SOUND = self.check_setting_str('Pushover', 'pushover_sound', 'pushover')

        self.USE_LIBNOTIFY = bool(self.check_setting_int('Libnotify', 'use_libnotify', 0))
        self.LIBNOTIFY_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('Libnotify', 'libnotify_notify_onsnatch', 0))
        self.LIBNOTIFY_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Libnotify', 'libnotify_notify_ondownload', 0))
        self.LIBNOTIFY_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Libnotify', 'libnotify_notify_onsubtitledownload', 0))

        self.USE_NMJ = bool(self.check_setting_int('NMJ', 'use_nmj', 0))
        self.NMJ_HOST = self.check_setting_str('NMJ', 'nmj_host', '')
        self.NMJ_DATABASE = self.check_setting_str('NMJ', 'nmj_database', '')
        self.NMJ_MOUNT = self.check_setting_str('NMJ', 'nmj_mount', '')

        self.USE_NMJv2 = bool(self.check_setting_int('NMJv2', 'use_nmjv2', 0))
        self.NMJv2_HOST = self.check_setting_str('NMJv2', 'nmjv2_host', '')
        self.NMJv2_DATABASE = self.check_setting_str('NMJv2', 'nmjv2_database', '')
        self.NMJv2_DBLOC = self.check_setting_str('NMJv2', 'nmjv2_dbloc', '')

        self.USE_SYNOINDEX = bool(self.check_setting_int('Synology', 'use_synoindex', 0))

        self.USE_SYNOLOGYNOTIFIER = bool(
            self.check_setting_int('SynologyNotifier', 'use_synologynotifier', 0))
        self.SYNOLOGYNOTIFIER_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('SynologyNotifier', 'synologynotifier_notify_onsnatch', 0))
        self.SYNOLOGYNOTIFIER_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('SynologyNotifier', 'synologynotifier_notify_ondownload', 0))
        self.SYNOLOGYNOTIFIER_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('SynologyNotifier', 'synologynotifier_notify_onsubtitledownload', 0))

        self.THETVDB_APITOKEN = self.check_setting_str('theTVDB', 'thetvdb_apitoken', '')

        self.USE_TRAKT = bool(self.check_setting_int('Trakt', 'use_trakt', 0))
        self.TRAKT_USERNAME = self.check_setting_str('Trakt', 'trakt_username', '')
        self.TRAKT_ACCESS_TOKEN = self.check_setting_str('Trakt', 'trakt_access_token', '')
        self.TRAKT_REFRESH_TOKEN = self.check_setting_str('Trakt', 'trakt_refresh_token', '')
        self.TRAKT_REMOVE_WATCHLIST = bool(self.check_setting_int('Trakt', 'trakt_remove_watchlist', 0))
        self.TRAKT_REMOVE_SERIESLIST = bool(
            self.check_setting_int('Trakt', 'trakt_remove_serieslist', 0))
        self.TRAKT_REMOVE_SHOW_FROM_SICKRAGE = bool(
            self.check_setting_int('Trakt', 'trakt_remove_show_from_sickrage', 0))
        self.TRAKT_SYNC_WATCHLIST = bool(self.check_setting_int('Trakt', 'trakt_sync_watchlist', 0))
        self.TRAKT_METHOD_ADD = self.check_setting_int('Trakt', 'trakt_method_add', 0)
        self.TRAKT_START_PAUSED = bool(self.check_setting_int('Trakt', 'trakt_start_paused', 0))
        self.TRAKT_USE_RECOMMENDED = bool(self.check_setting_int('Trakt', 'trakt_use_recommended', 0))
        self.TRAKT_SYNC = bool(self.check_setting_int('Trakt', 'trakt_sync', 0))
        self.TRAKT_SYNC_REMOVE = bool(self.check_setting_int('Trakt', 'trakt_sync_remove', 0))
        self.TRAKT_DEFAULT_INDEXER = self.check_setting_int('Trakt', 'trakt_default_indexer', 1)
        self.TRAKT_TIMEOUT = self.check_setting_int('Trakt', 'trakt_timeout', 30)
        self.TRAKT_BLACKLIST_NAME = self.check_setting_str('Trakt', 'trakt_blacklist_name', '')

        self.USE_PYTIVO = bool(self.check_setting_int('pyTivo', 'use_pytivo', 0))
        self.PYTIVO_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('pyTivo', 'pytivo_notify_onsnatch', 0))
        self.PYTIVO_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('pyTivo', 'pytivo_notify_ondownload', 0))
        self.PYTIVO_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('pyTivo', 'pytivo_notify_onsubtitledownload', 0))
        self.PYTIVO_UPDATE_LIBRARY = bool(self.check_setting_int('pyTivo', 'pyTivo_update_library', 0))
        self.PYTIVO_HOST = self.check_setting_str('pyTivo', 'pytivo_host', '')
        self.PYTIVO_SHARE_NAME = self.check_setting_str('pyTivo', 'pytivo_share_name', '')
        self.PYTIVO_TIVO_NAME = self.check_setting_str('pyTivo', 'pytivo_tivo_name', '')

        self.USE_NMA = bool(self.check_setting_int('NMA', 'use_nma', 0))
        self.NMA_NOTIFY_ONSNATCH = bool(self.check_setting_int('NMA', 'nma_notify_onsnatch', 0))
        self.NMA_NOTIFY_ONDOWNLOAD = bool(self.check_setting_int('NMA', 'nma_notify_ondownload', 0))
        self.NMA_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('NMA', 'nma_notify_onsubtitledownload', 0))
        self.NMA_API = self.check_setting_str('NMA', 'nma_api', '')
        self.NMA_PRIORITY = self.check_setting_str('NMA', 'nma_priority', "0")

        self.USE_PUSHALOT = bool(self.check_setting_int('Pushalot', 'use_pushalot', 0))
        self.PUSHALOT_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('Pushalot', 'pushalot_notify_onsnatch', 0))
        self.PUSHALOT_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Pushalot', 'pushalot_notify_ondownload', 0))
        self.PUSHALOT_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Pushalot', 'pushalot_notify_onsubtitledownload', 0))
        self.PUSHALOT_AUTHORIZATIONTOKEN = self.check_setting_str('Pushalot',
                                                                  'pushalot_authorizationtoken', '')

        self.USE_PUSHBULLET = bool(self.check_setting_int('Pushbullet', 'use_pushbullet', 0))
        self.PUSHBULLET_NOTIFY_ONSNATCH = bool(
            self.check_setting_int('Pushbullet', 'pushbullet_notify_onsnatch', 0))
        self.PUSHBULLET_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Pushbullet', 'pushbullet_notify_ondownload', 0))
        self.PUSHBULLET_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Pushbullet', 'pushbullet_notify_onsubtitledownload', 0))
        self.PUSHBULLET_API = self.check_setting_str('Pushbullet', 'pushbullet_api', '')
        self.PUSHBULLET_DEVICE = self.check_setting_str('Pushbullet', 'pushbullet_device', '')

        # self.emailself.notifyself.settings        self.USE_EMAIL= bool(self.check_setting_int('Email', 'use_email', 0))
        self.EMAIL_NOTIFY_ONSNATCH = bool(self.check_setting_int('Email', 'email_notify_onsnatch', 0))
        self.EMAIL_NOTIFY_ONDOWNLOAD = bool(
            self.check_setting_int('Email', 'email_notify_ondownload', 0))
        self.EMAIL_NOTIFY_ONSUBTITLEDOWNLOAD = bool(
            self.check_setting_int('Email', 'email_notify_onsubtitledownload', 0))
        self.EMAIL_HOST = self.check_setting_str('Email', 'email_host', '')
        self.EMAIL_PORT = self.check_setting_int('Email', 'email_port', 25)
        self.EMAIL_TLS = bool(self.check_setting_int('Email', 'email_tls', 0))
        self.EMAIL_USER = self.check_setting_str('Email', 'email_user', '')
        self.EMAIL_PASSWORD = self.check_setting_str('Email', 'email_password', '')
        self.EMAIL_FROM = self.check_setting_str('Email', 'email_from', '')
        self.EMAIL_LIST = self.check_setting_str('Email', 'email_list', '')

        self.USE_SUBTITLES = bool(self.check_setting_int('Subtitles', 'use_subtitles', 0))
        self.SUBTITLES_LANGUAGES = self.check_setting_str('Subtitles', 'subtitles_languages', '').split(
            ',')
        self.SUBTITLES_DIR = self.check_setting_str('Subtitles', 'subtitles_dir', '')
        self.SUBTITLES_SERVICES_LIST = self.check_setting_str('Subtitles', 'subtitles_services_list',
                                                              '').split(
            ',')
        self.SUBTITLES_DEFAULT = bool(self.check_setting_int('Subtitles', 'subtitles_default', 0))
        self.SUBTITLES_HISTORY = bool(self.check_setting_int('Subtitles', 'subtitles_history', 0))
        self.SUBTITLES_HEARING_IMPAIRED = bool(
            self.check_setting_int('Subtitles', 'subtitles_hearing_impaired', 0))
        self.EMBEDDED_SUBTITLES_ALL = bool(
            self.check_setting_int('Subtitles', 'embedded_subtitles_all', 0))
        self.SUBTITLES_MULTI = bool(self.check_setting_int('Subtitles', 'subtitles_multi', 1))
        self.SUBTITLES_SERVICES_ENABLED = [int(x) for x in
                                           self.check_setting_str('Subtitles', 'subtitles_services_enabled',
                                                                  '').split('|') if x]
        self.SUBTITLES_EXTRA_SCRIPTS = [x.strip() for x in
                                        self.check_setting_str('Subtitles', 'subtitles_extra_scripts',
                                                               '').split('|') if x.strip()]

        self.ADDIC7ED_USER = self.check_setting_str('Subtitles', 'addic7ed_username', '')
        self.ADDIC7ED_PASS = self.check_setting_str('Subtitles', 'addic7ed_password', '')

        self.LEGENDASTV_USER = self.check_setting_str('Subtitles', 'legendastv_username', '')
        self.LEGENDASTV_PASS = self.check_setting_str('Subtitles', 'legendastv_password', '')

        self.ITASA_USER = self.check_setting_str('Subtitles', 'itasa_username', '')
        self.ITASA_PASS = self.check_setting_str('Subtitles', 'itasa_password', '')

        self.OPENSUBTITLES_USER = self.check_setting_str('Subtitles', 'opensubtitles_username', '')
        self.OPENSUBTITLES_PASS = self.check_setting_str('Subtitles', 'opensubtitles_password', '')

        self.USE_FAILED_DOWNLOADS = bool(
            self.check_setting_int('FailedDownloads', 'use_failed_downloads', 0))
        self.DELETE_FAILED = bool(self.check_setting_int('FailedDownloads', 'delete_failed', 0))

        self.REQUIRE_WORDS = self.check_setting_str('General', 'require_words', '')
        self.IGNORE_WORDS = self.check_setting_str('General', 'ignore_words',
                                                   'german,french,core2hd,dutch,swedish,reenc,MrLss')
        self.IGNORED_SUBS_LIST = self.check_setting_str('General', 'ignored_subs_list',
                                                        'dk,fin,heb,kor,nor,nordic,pl,swe')

        self.CALENDAR_UNPROTECTED = bool(self.check_setting_int('General', 'calendar_unprotected', 0))
        self.CALENDAR_ICONS = bool(self.check_setting_int('General', 'calendar_icons', 0))

        self.NO_RESTART = bool(self.check_setting_int('General', 'no_restart', 0))
        self.EXTRA_SCRIPTS = [x.strip() for x in
                              self.check_setting_str('General', 'extra_scripts', '').split('|') if x.strip()]
        self.USE_LISTVIEW = bool(self.check_setting_int('General', 'use_listview', 0))

        self.USE_ANIDB = bool(self.check_setting_int('ANIDB', 'use_anidb', 0))
        self.ANIDB_USERNAME = self.check_setting_str('ANIDB', 'anidb_username', '')
        self.ANIDB_PASSWORD = self.check_setting_str('ANIDB', 'anidb_password', '')
        self.ANIDB_USE_MYLIST = bool(self.check_setting_int('ANIDB', 'anidb_use_mylist', 0))

        self.ANIME_SPLIT_HOME = bool(self.check_setting_int('ANIME', 'anime_split_home', 0))

        self.HOME_LAYOUT = self.check_setting_str('GUI', 'home_layout', 'poster')
        self.HISTORY_LAYOUT = self.check_setting_str('GUI', 'history_layout', 'detailed')
        self.HISTORY_LIMIT = self.check_setting_str('GUI', 'history_limit', '100')
        self.DISPLAY_SHOW_SPECIALS = bool(self.check_setting_int('GUI', 'display_show_specials', 1))
        self.COMING_EPS_LAYOUT = self.check_setting_str('GUI', 'coming_eps_layout', 'banner')
        self.COMING_EPS_DISPLAY_PAUSED = bool(
            self.check_setting_int('GUI', 'coming_eps_display_paused', 0))
        self.COMING_EPS_SORT = self.check_setting_str('GUI', 'coming_eps_sort', 'date')
        self.COMING_EPS_MISSED_RANGE = self.check_setting_int('GUI', 'coming_eps_missed_range', 7)
        self.FUZZY_DATING = bool(self.check_setting_int('GUI', 'fuzzy_dating', 0))
        self.TRIM_ZERO = bool(self.check_setting_int('GUI', 'trim_zero', 0))
        self.DATE_PRESET = self.check_setting_str('GUI', 'date_preset', '%x')
        self.TIME_PRESET_W_SECONDS = self.check_setting_str('GUI', 'time_preset', '%I:%M:%S%p')
        self.TIME_PRESET = self.TIME_PRESET_W_SECONDS.replace(":%S", "")
        self.TIMEZONE_DISPLAY = self.check_setting_str('GUI', 'timezone_display', 'local')
        self.POSTER_SORTBY = self.check_setting_str('GUI', 'poster_sortby', 'name')
        self.POSTER_SORTDIR = self.check_setting_int('GUI', 'poster_sortdir', 1)
        self.FILTER_ROW = bool(self.check_setting_int('GUI', 'filter_row', 1))
        self.DISPLAY_ALL_SEASONS = bool(self.check_setting_int('General', 'display_all_seasons', 1))

        self.RANDOM_USER_AGENT = bool(self.check_setting_int('General', 'random_user_agent', self.RANDOM_USER_AGENT))

        self.QUALITY_SIZES = self.check_setting_pickle('Quality', 'sizes', Quality.qualitySizes)

        self.CUSTOM_PROVIDERS = self.check_setting_str('Providers', 'custom_providers', '')

        sickrage.srCore.providersDict.load()
        for providerID, providerObj in sickrage.srCore.providersDict.all().items():
            providerSettings = self.check_setting_str('Providers', providerID) or {}
            for k, v in providerSettings.items():
                providerSettings[k] = autoType(v)

            [providerObj.__dict__.update({x: providerSettings[x]}) for x in
             set(providerObj.__dict__).intersection(providerSettings)]

        # order providers
        sickrage.srCore.providersDict.provider_order = self.check_setting_str('Providers', 'providers_order', [])

        for metadataProviderID, metadataProviderObj in sickrage.srCore.metadataProvidersDict.items():
            metadataProviderObj.set_config(
                self.check_setting_str('MetadataProviders', metadataProviderID, '0|0|0|0|0|0|0|0|0|0|0')
            )

        # mark config settings loaded
        self.loaded = True

        # save config settings
        self.save()

    def save(self):
        # dont bother saving settings if there not loaded
        if not self.loaded:
            return

        new_config = ConfigObj(sickrage.CONFIG_FILE, indent_type='  ')
        new_config.clear()

        sickrage.srCore.srLogger.debug("Saving all settings to disk")

        new_config['General'] = {}
        new_config['General']['config_version'] = self.CONFIG_VERSION
        new_config['General']['encryption_version'] = int(self.ENCRYPTION_VERSION)
        new_config['General']['encryption_secret'] = self.ENCRYPTION_SECRET
        new_config['General']['last_db_compact'] = self.LAST_DB_COMPACT
        new_config['General']['git_autoissues'] = int(self.GIT_AUTOISSUES)
        new_config['General']['git_username'] = self.GIT_USERNAME
        new_config['General']['git_password'] = self.GIT_PASSWORD
        new_config['General']['git_reset'] = int(self.GIT_RESET)
        new_config['General']['git_newver'] = int(self.GIT_NEWVER)
        new_config['General']['log_nr'] = int(self.LOG_NR)
        new_config['General']['log_size'] = int(self.LOG_SIZE)
        new_config['General']['socket_timeout'] = self.SOCKET_TIMEOUT
        new_config['General']['web_port'] = self.WEB_PORT
        new_config['General']['web_host'] = self.WEB_HOST
        new_config['General']['web_ipv6'] = int(self.WEB_IPV6)
        new_config['General']['web_log'] = int(self.WEB_LOG)
        new_config['General']['web_root'] = self.WEB_ROOT
        new_config['General']['web_username'] = self.WEB_USERNAME
        new_config['General']['web_password'] = self.WEB_PASSWORD
        new_config['General']['web_cookie_secret'] = self.WEB_COOKIE_SECRET
        new_config['General']['web_use_gzip'] = int(self.WEB_USE_GZIP)
        new_config['General']['ssl_verify'] = int(self.SSL_VERIFY)
        new_config['General']['download_url'] = self.DOWNLOAD_URL
        new_config['General']['cpu_preset'] = self.CPU_PRESET
        new_config['General']['anon_redirect'] = self.ANON_REDIRECT
        new_config['General']['api_key'] = self.API_KEY
        new_config['General']['debug'] = int(sickrage.DEBUG)
        new_config['General']['default_page'] = self.DEFAULT_PAGE
        new_config['General']['enable_https'] = int(self.ENABLE_HTTPS)
        new_config['General']['https_cert'] = self.HTTPS_CERT
        new_config['General']['https_key'] = self.HTTPS_KEY
        new_config['General']['handle_reverse_proxy'] = int(self.HANDLE_REVERSE_PROXY)
        new_config['General']['use_nzbs'] = int(self.USE_NZBS)
        new_config['General']['use_torrents'] = int(self.USE_TORRENTS)
        new_config['General']['nzb_method'] = self.NZB_METHOD
        new_config['General']['torrent_method'] = self.TORRENT_METHOD
        new_config['General']['usenet_retention'] = int(self.USENET_RETENTION)
        new_config['General']['autopostprocessor_frequency'] = int(self.AUTOPOSTPROCESSOR_FREQ)
        new_config['General']['dailysearch_frequency'] = int(self.DAILY_SEARCHER_FREQ)
        new_config['General']['backlog_frequency'] = int(self.BACKLOG_SEARCHER_FREQ)
        new_config['General']['update_frequency'] = int(self.VERSION_UPDATER_FREQ)
        new_config['General']['showupdate_hour'] = int(self.SHOWUPDATE_HOUR)
        new_config['General']['showupdate_stale'] = int(self.SHOWUPDATE_STALE)
        new_config['General']['download_propers'] = int(self.DOWNLOAD_PROPERS)
        new_config['General']['enable_rss_cache'] = int(self.ENABLE_RSS_CACHE)
        new_config['General']['randomize_providers'] = int(self.RANDOMIZE_PROVIDERS)
        new_config['General']['check_propers_interval'] = self.PROPER_SEARCHER_INTERVAL
        new_config['General']['allow_high_priority'] = int(self.ALLOW_HIGH_PRIORITY)
        new_config['General']['skip_removed_files'] = int(self.SKIP_REMOVED_FILES)
        new_config['General']['quality_default'] = int(self.QUALITY_DEFAULT)
        new_config['General']['status_default'] = int(self.STATUS_DEFAULT)
        new_config['General']['status_default_after'] = int(self.STATUS_DEFAULT_AFTER)
        new_config['General']['flatten_folders_default'] = int(self.FLATTEN_FOLDERS_DEFAULT)
        new_config['General']['indexer_default'] = int(self.INDEXER_DEFAULT)
        new_config['General']['indexer_timeout'] = int(self.INDEXER_TIMEOUT)
        new_config['General']['anime_default'] = int(self.ANIME_DEFAULT)
        new_config['General']['scene_default'] = int(self.SCENE_DEFAULT)
        new_config['General']['archive_default'] = int(self.ARCHIVE_DEFAULT)
        new_config['General']['version_notify'] = int(self.VERSION_NOTIFY)
        new_config['General']['auto_update'] = int(self.AUTO_UPDATE)
        new_config['General']['notify_on_update'] = int(self.NOTIFY_ON_UPDATE)
        new_config['General']['naming_strip_year'] = int(self.NAMING_STRIP_YEAR)
        new_config['General']['naming_pattern'] = self.NAMING_PATTERN
        new_config['General']['naming_custom_abd'] = int(self.NAMING_CUSTOM_ABD)
        new_config['General']['naming_abd_pattern'] = self.NAMING_ABD_PATTERN
        new_config['General']['naming_custom_sports'] = int(self.NAMING_CUSTOM_SPORTS)
        new_config['General']['naming_sports_pattern'] = self.NAMING_SPORTS_PATTERN
        new_config['General']['naming_custom_anime'] = int(self.NAMING_CUSTOM_ANIME)
        new_config['General']['naming_anime_pattern'] = self.NAMING_ANIME_PATTERN
        new_config['General']['naming_multi_ep'] = int(self.NAMING_MULTI_EP)
        new_config['General']['naming_anime_multi_ep'] = int(self.NAMING_ANIME_MULTI_EP)
        new_config['General']['naming_anime'] = int(self.NAMING_ANIME)
        new_config['General']['indexerDefaultLang'] = self.INDEXER_DEFAULT_LANGUAGE
        new_config['General']['ep_default_deleted_status'] = int(self.EP_DEFAULT_DELETED_STATUS)
        new_config['General']['launch_browser'] = int(self.LAUNCH_BROWSER)
        new_config['General']['trash_remove_show'] = int(self.TRASH_REMOVE_SHOW)
        new_config['General']['trash_rotate_logs'] = int(self.TRASH_ROTATE_LOGS)
        new_config['General']['sort_article'] = int(self.SORT_ARTICLE)
        new_config['General']['proxy_setting'] = self.PROXY_SETTING
        new_config['General']['proxy_indexers'] = int(self.PROXY_INDEXERS)
        new_config['General']['use_listview'] = int(self.USE_LISTVIEW)
        new_config['General']['backlog_days'] = int(self.BACKLOG_DAYS)
        new_config['General']['root_dirs'] = self.ROOT_DIRS
        new_config['General']['tv_download_dir'] = self.TV_DOWNLOAD_DIR
        new_config['General']['keep_processed_dir'] = int(self.KEEP_PROCESSED_DIR)
        new_config['General']['process_method'] = self.PROCESS_METHOD
        new_config['General']['del_rar_contents'] = int(self.DELRARCONTENTS)
        new_config['General']['move_associated_files'] = int(self.MOVE_ASSOCIATED_FILES)
        new_config['General']['sync_files'] = self.SYNC_FILES
        new_config['General']['postpone_if_sync_files'] = int(self.POSTPONE_IF_SYNC_FILES)
        new_config['General']['nfo_rename'] = int(self.NFO_RENAME)
        new_config['General']['process_automatically'] = int(self.PROCESS_AUTOMATICALLY)
        new_config['General']['no_delete'] = int(self.NO_DELETE)
        new_config['General']['unpack'] = int(self.UNPACK)
        new_config['General']['rename_episodes'] = int(self.RENAME_EPISODES)
        new_config['General']['airdate_episodes'] = int(self.AIRDATE_EPISODES)
        new_config['General']['file_timestamp_timezone'] = self.FILE_TIMESTAMP_TIMEZONE
        new_config['General']['create_missing_show_dirs'] = int(self.CREATE_MISSING_SHOW_DIRS)
        new_config['General']['add_shows_wo_dir'] = int(self.ADD_SHOWS_WO_DIR)
        new_config['General']['extra_scripts'] = '|'.join(self.EXTRA_SCRIPTS)
        new_config['General']['pip_path'] = self.PIP_PATH
        new_config['General']['git_path'] = self.GIT_PATH
        new_config['General']['ignore_words'] = self.IGNORE_WORDS
        new_config['General']['require_words'] = self.REQUIRE_WORDS
        new_config['General']['ignored_subs_list'] = self.IGNORED_SUBS_LIST
        new_config['General']['calendar_unprotected'] = int(self.CALENDAR_UNPROTECTED)
        new_config['General']['calendar_icons'] = int(self.CALENDAR_ICONS)
        new_config['General']['no_restart'] = int(self.NO_RESTART)
        new_config['General']['developer'] = int(sickrage.DEVELOPER)
        new_config['General']['display_all_seasons'] = int(self.DISPLAY_ALL_SEASONS)
        new_config['General']['random_user_agent'] = int(self.RANDOM_USER_AGENT)

        new_config['GUI'] = {}
        new_config['GUI']['gui_name'] = self.GUI_NAME
        new_config['GUI']['theme_name'] = self.THEME_NAME
        new_config['GUI']['home_layout'] = self.HOME_LAYOUT
        new_config['GUI']['history_layout'] = self.HISTORY_LAYOUT
        new_config['GUI']['history_limit'] = self.HISTORY_LIMIT
        new_config['GUI']['display_show_specials'] = int(self.DISPLAY_SHOW_SPECIALS)
        new_config['GUI']['coming_eps_layout'] = self.COMING_EPS_LAYOUT
        new_config['GUI']['coming_eps_display_paused'] = int(self.COMING_EPS_DISPLAY_PAUSED)
        new_config['GUI']['coming_eps_sort'] = self.COMING_EPS_SORT
        new_config['GUI']['coming_eps_missed_range'] = int(self.COMING_EPS_MISSED_RANGE)
        new_config['GUI']['fuzzy_dating'] = int(self.FUZZY_DATING)
        new_config['GUI']['trim_zero'] = int(self.TRIM_ZERO)
        new_config['GUI']['date_preset'] = self.DATE_PRESET
        new_config['GUI']['time_preset'] = self.TIME_PRESET_W_SECONDS
        new_config['GUI']['timezone_display'] = self.TIMEZONE_DISPLAY
        new_config['GUI']['poster_sortby'] = self.POSTER_SORTBY
        new_config['GUI']['poster_sortdir'] = self.POSTER_SORTDIR
        new_config['GUI']['filter_row'] = int(self.FILTER_ROW)

        new_config['Blackhole'] = {}
        new_config['Blackhole']['nzb_dir'] = self.NZB_DIR
        new_config['Blackhole']['torrent_dir'] = self.TORRENT_DIR

        new_config['NZBs'] = {}
        new_config['NZBs']['nzbs'] = int(self.NZBS)
        new_config['NZBs']['nzbs_uid'] = self.NZBS_UID
        new_config['NZBs']['nzbs_hash'] = self.NZBS_HASH

        new_config['Newzbin'] = {}
        new_config['Newzbin']['newzbin'] = int(self.NEWZBIN)
        new_config['Newzbin']['newzbin_username'] = self.NEWZBIN_USERNAME
        new_config['Newzbin']['newzbin_password'] = self.NEWZBIN_PASSWORD

        new_config['SABnzbd'] = {}
        new_config['SABnzbd']['sab_username'] = self.SAB_USERNAME
        new_config['SABnzbd']['sab_password'] = self.SAB_PASSWORD
        new_config['SABnzbd']['sab_apikey'] = self.SAB_APIKEY
        new_config['SABnzbd']['sab_category'] = self.SAB_CATEGORY
        new_config['SABnzbd']['sab_category_backlog'] = self.SAB_CATEGORY_BACKLOG
        new_config['SABnzbd']['sab_category_anime'] = self.SAB_CATEGORY_ANIME
        new_config['SABnzbd']['sab_category_anime_backlog'] = self.SAB_CATEGORY_ANIME_BACKLOG
        new_config['SABnzbd']['sab_host'] = self.SAB_HOST
        new_config['SABnzbd']['sab_forced'] = int(self.SAB_FORCED)

        new_config['NZBget'] = {}
        new_config['NZBget']['nzbget_username'] = self.NZBGET_USERNAME
        new_config['NZBget']['nzbget_password'] = self.NZBGET_PASSWORD
        new_config['NZBget']['nzbget_category'] = self.NZBGET_CATEGORY
        new_config['NZBget']['nzbget_category_backlog'] = self.NZBGET_CATEGORY_BACKLOG
        new_config['NZBget']['nzbget_category_anime'] = self.NZBGET_CATEGORY_ANIME
        new_config['NZBget']['nzbget_category_anime_backlog'] = self.NZBGET_CATEGORY_ANIME_BACKLOG
        new_config['NZBget']['nzbget_host'] = self.NZBGET_HOST
        new_config['NZBget']['nzbget_use_https'] = int(self.NZBGET_USE_HTTPS)
        new_config['NZBget']['nzbget_priority'] = self.NZBGET_PRIORITY

        new_config['TORRENT'] = {}
        new_config['TORRENT']['torrent_username'] = self.TORRENT_USERNAME
        new_config['TORRENT']['torrent_password'] = self.TORRENT_PASSWORD
        new_config['TORRENT']['torrent_host'] = self.TORRENT_HOST
        new_config['TORRENT']['torrent_path'] = self.TORRENT_PATH
        new_config['TORRENT']['torrent_seed_time'] = int(self.TORRENT_SEED_TIME)
        new_config['TORRENT']['torrent_paused'] = int(self.TORRENT_PAUSED)
        new_config['TORRENT']['torrent_high_bandwidth'] = int(self.TORRENT_HIGH_BANDWIDTH)
        new_config['TORRENT']['torrent_label'] = self.TORRENT_LABEL
        new_config['TORRENT']['torrent_label_anime'] = self.TORRENT_LABEL_ANIME
        new_config['TORRENT']['torrent_verify_cert'] = int(self.TORRENT_VERIFY_CERT)
        new_config['TORRENT']['torrent_rpcurl'] = self.TORRENT_RPCURL
        new_config['TORRENT']['torrent_auth_type'] = self.TORRENT_AUTH_TYPE
        new_config['TORRENT']['torrent_trackers'] = self.TORRENT_TRACKERS

        new_config['KODI'] = {}
        new_config['KODI']['use_kodi'] = int(self.USE_KODI)
        new_config['KODI']['kodi_always_on'] = int(self.KODI_ALWAYS_ON)
        new_config['KODI']['kodi_notify_onsnatch'] = int(self.KODI_NOTIFY_ONSNATCH)
        new_config['KODI']['kodi_notify_ondownload'] = int(self.KODI_NOTIFY_ONDOWNLOAD)
        new_config['KODI']['kodi_notify_onsubtitledownload'] = int(self.KODI_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['KODI']['kodi_update_library'] = int(self.KODI_UPDATE_LIBRARY)
        new_config['KODI']['kodi_update_full'] = int(self.KODI_UPDATE_FULL)
        new_config['KODI']['kodi_update_onlyfirst'] = int(self.KODI_UPDATE_ONLYFIRST)
        new_config['KODI']['kodi_host'] = self.KODI_HOST
        new_config['KODI']['kodi_username'] = self.KODI_USERNAME
        new_config['KODI']['kodi_password'] = self.KODI_PASSWORD

        new_config['Plex'] = {}
        new_config['Plex']['use_plex'] = int(self.USE_PLEX)
        new_config['Plex']['plex_notify_onsnatch'] = int(self.PLEX_NOTIFY_ONSNATCH)
        new_config['Plex']['plex_notify_ondownload'] = int(self.PLEX_NOTIFY_ONDOWNLOAD)
        new_config['Plex']['plex_notify_onsubtitledownload'] = int(self.PLEX_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Plex']['plex_update_library'] = int(self.PLEX_UPDATE_LIBRARY)
        new_config['Plex']['plex_server_host'] = self.PLEX_SERVER_HOST
        new_config['Plex']['plex_server_token'] = self.PLEX_SERVER_TOKEN
        new_config['Plex']['plex_host'] = self.PLEX_HOST
        new_config['Plex']['plex_username'] = self.PLEX_USERNAME
        new_config['Plex']['plex_password'] = self.PLEX_PASSWORD

        new_config['Emby'] = {}
        new_config['Emby']['use_emby'] = int(self.USE_EMBY)
        new_config['Emby']['emby_host'] = self.EMBY_HOST
        new_config['Emby']['emby_apikey'] = self.EMBY_APIKEY

        new_config['Growl'] = {}
        new_config['Growl']['use_growl'] = int(self.USE_GROWL)
        new_config['Growl']['growl_notify_onsnatch'] = int(self.GROWL_NOTIFY_ONSNATCH)
        new_config['Growl']['growl_notify_ondownload'] = int(self.GROWL_NOTIFY_ONDOWNLOAD)
        new_config['Growl']['growl_notify_onsubtitledownload'] = int(self.GROWL_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Growl']['growl_host'] = self.GROWL_HOST
        new_config['Growl']['growl_password'] = self.GROWL_PASSWORD

        new_config['FreeMobile'] = {}
        new_config['FreeMobile']['use_freemobile'] = int(self.USE_FREEMOBILE)
        new_config['FreeMobile']['freemobile_notify_onsnatch'] = int(self.FREEMOBILE_NOTIFY_ONSNATCH)
        new_config['FreeMobile']['freemobile_notify_ondownload'] = int(self.FREEMOBILE_NOTIFY_ONDOWNLOAD)
        new_config['FreeMobile']['freemobile_notify_onsubtitledownload'] = int(
            self.FREEMOBILE_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['FreeMobile']['freemobile_id'] = self.FREEMOBILE_ID
        new_config['FreeMobile']['freemobile_apikey'] = self.FREEMOBILE_APIKEY

        new_config['Prowl'] = {}
        new_config['Prowl']['use_prowl'] = int(self.USE_PROWL)
        new_config['Prowl']['prowl_notify_onsnatch'] = int(self.PROWL_NOTIFY_ONSNATCH)
        new_config['Prowl']['prowl_notify_ondownload'] = int(self.PROWL_NOTIFY_ONDOWNLOAD)
        new_config['Prowl']['prowl_notify_onsubtitledownload'] = int(self.PROWL_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Prowl']['prowl_api'] = self.PROWL_API
        new_config['Prowl']['prowl_priority'] = self.PROWL_PRIORITY

        new_config['Twitter'] = {}
        new_config['Twitter']['use_twitter'] = int(self.USE_TWITTER)
        new_config['Twitter']['twitter_notify_onsnatch'] = int(self.TWITTER_NOTIFY_ONSNATCH)
        new_config['Twitter']['twitter_notify_ondownload'] = int(self.TWITTER_NOTIFY_ONDOWNLOAD)
        new_config['Twitter']['twitter_notify_onsubtitledownload'] = int(
            self.TWITTER_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Twitter']['twitter_username'] = self.TWITTER_USERNAME
        new_config['Twitter']['twitter_password'] = self.TWITTER_PASSWORD
        new_config['Twitter']['twitter_prefix'] = self.TWITTER_PREFIX
        new_config['Twitter']['twitter_dmto'] = self.TWITTER_DMTO
        new_config['Twitter']['twitter_usedm'] = int(self.TWITTER_USEDM)

        new_config['Boxcar'] = {}
        new_config['Boxcar']['use_boxcar'] = int(self.USE_BOXCAR)
        new_config['Boxcar']['boxcar_notify_onsnatch'] = int(self.BOXCAR_NOTIFY_ONSNATCH)
        new_config['Boxcar']['boxcar_notify_ondownload'] = int(self.BOXCAR_NOTIFY_ONDOWNLOAD)
        new_config['Boxcar']['boxcar_notify_onsubtitledownload'] = int(self.BOXCAR_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Boxcar']['boxcar_username'] = self.BOXCAR_USERNAME

        new_config['Boxcar2'] = {}
        new_config['Boxcar2']['use_boxcar2'] = int(self.USE_BOXCAR2)
        new_config['Boxcar2']['boxcar2_notify_onsnatch'] = int(self.BOXCAR2_NOTIFY_ONSNATCH)
        new_config['Boxcar2']['boxcar2_notify_ondownload'] = int(self.BOXCAR2_NOTIFY_ONDOWNLOAD)
        new_config['Boxcar2']['boxcar2_notify_onsubtitledownload'] = int(
            self.BOXCAR2_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Boxcar2']['boxcar2_accesstoken'] = self.BOXCAR2_ACCESSTOKEN

        new_config['Pushover'] = {}
        new_config['Pushover']['use_pushover'] = int(self.USE_PUSHOVER)
        new_config['Pushover']['pushover_notify_onsnatch'] = int(self.PUSHOVER_NOTIFY_ONSNATCH)
        new_config['Pushover']['pushover_notify_ondownload'] = int(self.PUSHOVER_NOTIFY_ONDOWNLOAD)
        new_config['Pushover']['pushover_notify_onsubtitledownload'] = int(
            self.PUSHOVER_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Pushover']['pushover_userkey'] = self.PUSHOVER_USERKEY
        new_config['Pushover']['pushover_apikey'] = self.PUSHOVER_APIKEY
        new_config['Pushover']['pushover_device'] = self.PUSHOVER_DEVICE
        new_config['Pushover']['pushover_sound'] = self.PUSHOVER_SOUND

        new_config['Libnotify'] = {}
        new_config['Libnotify']['use_libnotify'] = int(self.USE_LIBNOTIFY)
        new_config['Libnotify']['libnotify_notify_onsnatch'] = int(self.LIBNOTIFY_NOTIFY_ONSNATCH)
        new_config['Libnotify']['libnotify_notify_ondownload'] = int(self.LIBNOTIFY_NOTIFY_ONDOWNLOAD)
        new_config['Libnotify']['libnotify_notify_onsubtitledownload'] = int(
            self.LIBNOTIFY_NOTIFY_ONSUBTITLEDOWNLOAD)

        new_config['NMJ'] = {}
        new_config['NMJ']['use_nmj'] = int(self.USE_NMJ)
        new_config['NMJ']['nmj_host'] = self.NMJ_HOST
        new_config['NMJ']['nmj_database'] = self.NMJ_DATABASE
        new_config['NMJ']['nmj_mount'] = self.NMJ_MOUNT

        new_config['NMJv2'] = {}
        new_config['NMJv2']['use_nmjv2'] = int(self.USE_NMJv2)
        new_config['NMJv2']['nmjv2_host'] = self.NMJv2_HOST
        new_config['NMJv2']['nmjv2_database'] = self.NMJv2_DATABASE
        new_config['NMJv2']['nmjv2_dbloc'] = self.NMJv2_DBLOC

        new_config['Synology'] = {}
        new_config['Synology']['use_synoindex'] = int(self.USE_SYNOINDEX)

        new_config['SynologyNotifier'] = {}
        new_config['SynologyNotifier']['use_synologynotifier'] = int(self.USE_SYNOLOGYNOTIFIER)
        new_config['SynologyNotifier']['synologynotifier_notify_onsnatch'] = int(
            self.SYNOLOGYNOTIFIER_NOTIFY_ONSNATCH)
        new_config['SynologyNotifier']['synologynotifier_notify_ondownload'] = int(
            self.SYNOLOGYNOTIFIER_NOTIFY_ONDOWNLOAD)
        new_config['SynologyNotifier']['synologynotifier_notify_onsubtitledownload'] = int(
            self.SYNOLOGYNOTIFIER_NOTIFY_ONSUBTITLEDOWNLOAD)

        new_config['theTVDB'] = {}
        new_config['theTVDB']['thetvdb_apitoken'] = self.THETVDB_APITOKEN

        new_config['Trakt'] = {}
        new_config['Trakt']['use_trakt'] = int(self.USE_TRAKT)
        new_config['Trakt']['trakt_username'] = self.TRAKT_USERNAME
        new_config['Trakt']['trakt_access_token'] = self.TRAKT_ACCESS_TOKEN
        new_config['Trakt']['trakt_refresh_token'] = self.TRAKT_REFRESH_TOKEN
        new_config['Trakt']['trakt_remove_watchlist'] = int(self.TRAKT_REMOVE_WATCHLIST)
        new_config['Trakt']['trakt_remove_serieslist'] = int(self.TRAKT_REMOVE_SERIESLIST)
        new_config['Trakt']['trakt_remove_show_from_sickrage'] = int(self.TRAKT_REMOVE_SHOW_FROM_SICKRAGE)
        new_config['Trakt']['trakt_sync_watchlist'] = int(self.TRAKT_SYNC_WATCHLIST)
        new_config['Trakt']['trakt_method_add'] = int(self.TRAKT_METHOD_ADD)
        new_config['Trakt']['trakt_start_paused'] = int(self.TRAKT_START_PAUSED)
        new_config['Trakt']['trakt_use_recommended'] = int(self.TRAKT_USE_RECOMMENDED)
        new_config['Trakt']['trakt_sync'] = int(self.TRAKT_SYNC)
        new_config['Trakt']['trakt_sync_remove'] = int(self.TRAKT_SYNC_REMOVE)
        new_config['Trakt']['trakt_default_indexer'] = int(self.TRAKT_DEFAULT_INDEXER)
        new_config['Trakt']['trakt_timeout'] = int(self.TRAKT_TIMEOUT)
        new_config['Trakt']['trakt_blacklist_name'] = self.TRAKT_BLACKLIST_NAME

        new_config['pyTivo'] = {}
        new_config['pyTivo']['use_pytivo'] = int(self.USE_PYTIVO)
        new_config['pyTivo']['pytivo_notify_onsnatch'] = int(self.PYTIVO_NOTIFY_ONSNATCH)
        new_config['pyTivo']['pytivo_notify_ondownload'] = int(self.PYTIVO_NOTIFY_ONDOWNLOAD)
        new_config['pyTivo']['pytivo_notify_onsubtitledownload'] = int(self.PYTIVO_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['pyTivo']['pyTivo_update_library'] = int(self.PYTIVO_UPDATE_LIBRARY)
        new_config['pyTivo']['pytivo_host'] = self.PYTIVO_HOST
        new_config['pyTivo']['pytivo_share_name'] = self.PYTIVO_SHARE_NAME
        new_config['pyTivo']['pytivo_tivo_name'] = self.PYTIVO_TIVO_NAME

        new_config['NMA'] = {}
        new_config['NMA']['use_nma'] = int(self.USE_NMA)
        new_config['NMA']['nma_notify_onsnatch'] = int(self.NMA_NOTIFY_ONSNATCH)
        new_config['NMA']['nma_notify_ondownload'] = int(self.NMA_NOTIFY_ONDOWNLOAD)
        new_config['NMA']['nma_notify_onsubtitledownload'] = int(self.NMA_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['NMA']['nma_api'] = self.NMA_API
        new_config['NMA']['nma_priority'] = self.NMA_PRIORITY

        new_config['Pushalot'] = {}
        new_config['Pushalot']['use_pushalot'] = int(self.USE_PUSHALOT)
        new_config['Pushalot']['pushalot_notify_onsnatch'] = int(self.PUSHALOT_NOTIFY_ONSNATCH)
        new_config['Pushalot']['pushalot_notify_ondownload'] = int(self.PUSHALOT_NOTIFY_ONDOWNLOAD)
        new_config['Pushalot']['pushalot_notify_onsubtitledownload'] = int(
            self.PUSHALOT_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Pushalot']['pushalot_authorizationtoken'] = self.PUSHALOT_AUTHORIZATIONTOKEN

        new_config['Pushbullet'] = {}
        new_config['Pushbullet']['use_pushbullet'] = int(self.USE_PUSHBULLET)
        new_config['Pushbullet']['pushbullet_notify_onsnatch'] = int(self.PUSHBULLET_NOTIFY_ONSNATCH)
        new_config['Pushbullet']['pushbullet_notify_ondownload'] = int(self.PUSHBULLET_NOTIFY_ONDOWNLOAD)
        new_config['Pushbullet']['pushbullet_notify_onsubtitledownload'] = int(
            self.PUSHBULLET_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Pushbullet']['pushbullet_api'] = self.PUSHBULLET_API
        new_config['Pushbullet']['pushbullet_device'] = self.PUSHBULLET_DEVICE

        new_config['Email'] = {}
        new_config['Email']['use_email'] = int(self.USE_EMAIL)
        new_config['Email']['email_notify_onsnatch'] = int(self.EMAIL_NOTIFY_ONSNATCH)
        new_config['Email']['email_notify_ondownload'] = int(self.EMAIL_NOTIFY_ONDOWNLOAD)
        new_config['Email']['email_notify_onsubtitledownload'] = int(self.EMAIL_NOTIFY_ONSUBTITLEDOWNLOAD)
        new_config['Email']['email_host'] = self.EMAIL_HOST
        new_config['Email']['email_port'] = int(self.EMAIL_PORT)
        new_config['Email']['email_tls'] = int(self.EMAIL_TLS)
        new_config['Email']['email_user'] = self.EMAIL_USER
        new_config['Email']['email_password'] = self.EMAIL_PASSWORD
        new_config['Email']['email_from'] = self.EMAIL_FROM
        new_config['Email']['email_list'] = self.EMAIL_LIST

        new_config['Subtitles'] = {}
        new_config['Subtitles']['use_subtitles'] = int(self.USE_SUBTITLES)
        new_config['Subtitles']['subtitles_languages'] = ','.join(self.SUBTITLES_LANGUAGES)
        new_config['Subtitles']['subtitles_services_list'] = ','.join(self.SUBTITLES_SERVICES_LIST)
        new_config['Subtitles']['subtitles_services_enabled'] = '|'.join(
            [str(x) for x in self.SUBTITLES_SERVICES_ENABLED])
        new_config['Subtitles']['subtitles_dir'] = self.SUBTITLES_DIR
        new_config['Subtitles']['subtitles_default'] = int(self.SUBTITLES_DEFAULT)
        new_config['Subtitles']['subtitles_history'] = int(self.SUBTITLES_HISTORY)
        new_config['Subtitles']['embedded_subtitles_all'] = int(self.EMBEDDED_SUBTITLES_ALL)
        new_config['Subtitles']['subtitles_hearing_impaired'] = int(self.SUBTITLES_HEARING_IMPAIRED)
        new_config['Subtitles']['subtitles_finder_frequency'] = int(self.SUBTITLE_SEARCHER_FREQ)
        new_config['Subtitles']['subtitles_multi'] = int(self.SUBTITLES_MULTI)
        new_config['Subtitles']['subtitles_extra_scripts'] = '|'.join(self.SUBTITLES_EXTRA_SCRIPTS)
        new_config['Subtitles']['addic7ed_username'] = self.ADDIC7ED_USER
        new_config['Subtitles']['addic7ed_password'] = self.ADDIC7ED_PASS
        new_config['Subtitles']['legendastv_username'] = self.LEGENDASTV_USER
        new_config['Subtitles']['legendastv_password'] = self.LEGENDASTV_PASS
        new_config['Subtitles']['itasa_username'] = self.ITASA_USER
        new_config['Subtitles']['itasa_password'] = self.ITASA_PASS
        new_config['Subtitles']['opensubtitles_username'] = self.OPENSUBTITLES_USER
        new_config['Subtitles']['opensubtitles_password'] = self.OPENSUBTITLES_PASS

        new_config['FailedDownloads'] = {}
        new_config['FailedDownloads']['use_failed_downloads'] = int(self.USE_FAILED_DOWNLOADS)
        new_config['FailedDownloads']['delete_failed'] = int(self.DELETE_FAILED)

        new_config['ANIDB'] = {}
        new_config['ANIDB']['use_anidb'] = int(self.USE_ANIDB)
        new_config['ANIDB']['anidb_username'] = self.ANIDB_USERNAME
        new_config['ANIDB']['anidb_password'] = self.ANIDB_PASSWORD
        new_config['ANIDB']['anidb_use_mylist'] = int(self.ANIDB_USE_MYLIST)

        new_config['ANIME'] = {}
        new_config['ANIME']['anime_split_home'] = int(self.ANIME_SPLIT_HOME)

        new_config['Quality'] = {}
        new_config['Quality']['sizes'] = pickle.dumps(self.QUALITY_SIZES)

        new_config['Providers'] = {}
        new_config['Providers']['providers_order'] = sickrage.srCore.providersDict.provider_order
        new_config['Providers']['custom_providers'] = self.CUSTOM_PROVIDERS

        provider_keys = ['enabled', 'confirmed', 'ranked', 'engrelease', 'onlyspasearch', 'sorting', 'options', 'ratio',
                         'minseed', 'minleech', 'freeleech', 'search_mode', 'search_fallback', 'enable_daily', 'key',
                         'enable_backlog', 'cat', 'subtitle', 'api_key', 'hash', 'digest', 'username', 'password',
                         'passkey', 'pin', 'reject_m2ts', 'enable_cookies', 'cookies']

        for providerID, providerObj in sickrage.srCore.providersDict.all().items():
            new_config['Providers'][providerID] = dict(
                [(x, providerObj.__dict__[x]) for x in provider_keys if hasattr(providerObj, x)])

        new_config['MetadataProviders'] = {}
        for metadataProviderID, metadataProviderObj in sickrage.srCore.metadataProvidersDict.items():
            new_config['MetadataProviders'][metadataProviderID] = metadataProviderObj.get_config()

        # encrypt settings
        new_config.walk(self.encrypt)
        new_config.write()

    def encrypt(self, section, key, _decrypt=False):
        """
        :rtype: basestring
        """

        if key in ['config_version', 'encryption_version', 'encryption_secret']:
            pass
        else:
            try:
                if self.ENCRYPTION_VERSION == 1:
                    unique_key1 = hex(uuid.getnode() ** 2)

                    if _decrypt:
                        section[key] = ''.join(
                            chr(ord(x) ^ ord(y)) for (x, y) in
                            izip(base64.decodestring(section[key]), cycle(unique_key1)))
                    else:
                        section[key] = base64.encodestring(
                            ''.join(chr(ord(x) ^ ord(y)) for (x, y) in izip(section[key], cycle(unique_key1)))).strip()
                elif self.ENCRYPTION_VERSION == 2:
                    if _decrypt:
                        section[key] = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in
                                               izip(base64.decodestring(section[key]),
                                                    cycle(sickrage.srCore.srConfig.ENCRYPTION_SECRET)))
                    else:
                        section[key] = base64.encodestring(
                            ''.join(chr(ord(x) ^ ord(y)) for (x, y) in izip(section[key], cycle(
                                sickrage.srCore.srConfig.ENCRYPTION_SECRET)))).strip()
            except:
                pass

    def decrypt(self, section, key):
        return self.encrypt(section, key, _decrypt=True)


class ConfigMigrator(srConfig):
    def __init__(self, configobj):
        """
        Initializes a config migrator that can take the config from the version indicated in the config
        file up to the latest version
        """
        super(ConfigMigrator, self).__init__()
        self.CONFIG_OBJ = configobj

        # check the version of the config
        self.config_version = self.check_setting_int('General', 'config_version', self.CONFIG_VERSION)
        self.expected_config_version = self.CONFIG_VERSION

        self.migration_names = {
            1: 'Sync backup number with version number',
            2: 'Sync backup number with version number',
            3: 'Sync backup number with version number',
            4: 'Sync backup number with version number',
            5: 'Sync backup number with version number',
            6: 'Sync backup number with version number',
            7: 'Sync backup number with version number',
            8: 'Use version 2 for password encryption',
            9: 'Rename slick gui template name to default',
            10: 'Add enabled attribute to metadata settings',
            11: 'Rename all metadata settings'
        }

    def migrate_config(self):
        """
        Calls each successive migration until the config is the same version as SB expects
        """

        if self.config_version > self.expected_config_version:
            sickrage.srCore.srLogger.error(
                """Your config version (%i) has been incremented past what this version of supports (%i).
                    If you have used other forks or a newer version of  your config file may be unusable due to their modifications.""" %
                (self.config_version, self.expected_config_version)
            )
            sys.exit(1)

        self.CONFIG_VERSION = self.config_version

        while self.config_version < self.expected_config_version:
            next_version = self.config_version + 1

            if next_version in self.migration_names:
                migration_name = ': ' + self.migration_names[next_version]
            else:
                migration_name = ''

            sickrage.srCore.srLogger.info("Backing up config before upgrade")
            if not backupVersionedFile(sickrage.CONFIG_FILE, self.config_version):
                sickrage.srCore.srLogger.exit("Config backup failed, abort upgrading config")
                sys.exit(1)
            else:
                sickrage.srCore.srLogger.info("Proceeding with upgrade")

            # do the migration, expect a method named _migrate_v<num>
            sickrage.srCore.srLogger.info("Migrating config up to version " + str(next_version) + migration_name)
            self.CONFIG_OBJ = getattr(self, '_migrate_v' + str(next_version))()
            self.config_version = next_version

            # update config version to newest
            self.CONFIG_VERSION = self.config_version

        return self.CONFIG_OBJ

    # Migration v1: Dummy migration to sync backup number with config version number
    def _migrate_v1(self):
        return self.CONFIG_OBJ

    # Migration v2: Dummy migration to sync backup number with config version number
    def _migrate_v2(self):
        return self.CONFIG_OBJ

    # Migration v3: Dummy migration to sync backup number with config version number
    def _migrate_v3(self):
        return self.CONFIG_OBJ

    # Migration v4: Dummy migration to sync backup number with config version number
    def _migrate_v4(self):
        return self.CONFIG_OBJ

    # Migration v5: Dummy migration to sync backup number with config version number
    def _migrate_v5(self):
        return self.CONFIG_OBJ

    # Migration v6: Dummy migration to sync backup number with config version number
    def _migrate_v6(self):
        return self.CONFIG_OBJ

    # Migration v6: Dummy migration to sync backup number with config version number
    def _migrate_v7(self):
        return self.CONFIG_OBJ

    # Migration v8: Use version 2 for password encryption
    def _migrate_v8(self):
        self.CONFIG_OBJ['General']['encryption_version'] = 2
        return self.CONFIG_OBJ

    # Migration v9: Rename gui template name from slick to default
    def _migrate_v9(self):
        self.CONFIG_OBJ['GUI']['gui_name'] = 'default'
        return self.CONFIG_OBJ

    # Migration v10: Metadata upgrade to add enabled attribute
    def _migrate_v10(self):
        """
        Updates metadata values to the new format
        Quick overview of what the upgrade does:

        new | old | description (new)
        ----+-----+--------------------
          1 |  1  | show metadata
          2 |  2  | episode metadata
          3 |  3  | show fanart
          4 |  4  | show poster
          5 |  5  | show banner
          6 |  6  | episode thumb
          7 |  7  | season poster
          8 |  8  | season banner
          9 |  9  | season all poster
         10 |  10 | season all banner
         11 |  -  | enabled

        Note that the ini places start at 1 while the list index starts at 0.
        old format: 0|0|0|0|0|0|0|0|0|0 -- 10 places
        new format: 0|0|0|0|0|0|0|0|0|0|0 -- 11 places
        """

        metadata_kodi = self.check_setting_str('General', 'metadata_kodi', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_kodi_12plus = self.check_setting_str('General', 'metadata_kodi_12plus', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_mediabrowser = self.check_setting_str('General', 'metadata_mediabrowser', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_ps3 = self.check_setting_str('General', 'metadata_ps3', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_wdtv = self.check_setting_str('General', 'metadata_wdtv', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_tivo = self.check_setting_str('General', 'metadata_tivo', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_mede8er = self.check_setting_str('General', 'metadata_mede8er', '0|0|0|0|0|0|0|0|0|0|0')

        def _migrate_metadata(metadata):
            cur_metadata = metadata.split('|')

            # if target has the old number of values, do upgrade
            if len(cur_metadata) == 10:
                # write new format
                cur_metadata.append('0')
                metadata = '|'.join(cur_metadata)
            elif len(cur_metadata) == 11:
                metadata = '|'.join(cur_metadata)
            else:
                metadata = '0|0|0|0|0|0|0|0|0|0|0'

            return metadata

        self.CONFIG_OBJ['General']['metadata_kodi'] = _migrate_metadata(metadata_kodi)
        self.CONFIG_OBJ['General']['metadata_kodi_12plus'] = _migrate_metadata(metadata_kodi_12plus)
        self.CONFIG_OBJ['General']['metadata_mediabrowser'] = _migrate_metadata(metadata_mediabrowser)
        self.CONFIG_OBJ['General']['metadata_ps3'] = _migrate_metadata(metadata_ps3)
        self.CONFIG_OBJ['General']['metadata_wdtv'] = _migrate_metadata(metadata_wdtv)
        self.CONFIG_OBJ['General']['metadata_tivo'] = _migrate_metadata(metadata_tivo)
        self.CONFIG_OBJ['General']['metadata_mede8er'] = _migrate_metadata(metadata_mede8er)

        return self.CONFIG_OBJ

    # Migration v11: Renames metadata setting keys
    def _migrate_v11(self):
        """
        Renames metadata setting keys
        """

        metadata_kodi = self.check_setting_str('General', 'metadata_kodi', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_kodi_12plus = self.check_setting_str('General', 'metadata_kodi_12plus', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_mediabrowser = self.check_setting_str('General', 'metadata_mediabrowser', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_ps3 = self.check_setting_str('General', 'metadata_ps3', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_wdtv = self.check_setting_str('General', 'metadata_wdtv', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_tivo = self.check_setting_str('General', 'metadata_tivo', '0|0|0|0|0|0|0|0|0|0|0')
        metadata_mede8er = self.check_setting_str('General', 'metadata_mede8er', '0|0|0|0|0|0|0|0|0|0|0')

        self.CONFIG_OBJ['MetadataProviders'] = {}
        self.CONFIG_OBJ['MetadataProviders']['kodi'] = metadata_kodi
        self.CONFIG_OBJ['MetadataProviders']['kodi_12plus'] = metadata_kodi_12plus
        self.CONFIG_OBJ['MetadataProviders']['mediabrowser'] = metadata_mediabrowser
        self.CONFIG_OBJ['MetadataProviders']['sony_ps3'] = metadata_ps3
        self.CONFIG_OBJ['MetadataProviders']['wdtv'] = metadata_wdtv
        self.CONFIG_OBJ['MetadataProviders']['tivo'] = metadata_tivo
        self.CONFIG_OBJ['MetadataProviders']['mede8er'] = metadata_mede8er

        return self.CONFIG_OBJ
