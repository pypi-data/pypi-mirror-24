# LICENSE
#
# This file is released in the Public Domain.
#
# In case of copyright claims you can use this license 
# to prove that intention is to have no copyright on this work and
# consider it to be in the Publc Domain.
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" rss module. """

from .launcher import Launcher
from .object import Default, Object
from .register import Register
from .clock import Repeater
from .space import launcher, runtime
from .url import get_url

try:
    import feedparser
except:
    pass

import botlib
import logging
import urllib

def init(*args, **kwargs):
    """ initialize the rss feed fetcher. """
    rss = RSS()
    rss.start()
    return rss

def shutdown(event):
    """ shutdown the rss feed fetcher. """
    rss = runtime.get("RSS", [])
    for item in rss:
        item.stop()

def get_feed(url):
    """ fetch a feed. """
    result = []
    if not url or not "http" in url:
        logging.warn("! %s is not an url." % url)
        return result
    try:
        result = feedparser.parse(get_url(url).data)
    except (ImportError, ConnectionError, urllib.error.URLError) as ex:
        logging.info("! feed %s %s" % (url, str(ex)))
        return result
    if "entries" in result:
        for entry in result["entries"]:
            yield Default(entry)

class Feed(Object):

    """ feed typed object. """

    pass

class RSS(Register, Launcher):

    """ RSS class for fetching rss feeds. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = str(type(self))

    def start(self, *args, **kwargs):
        """ start rss fetcher. """
        repeater = Repeater(600, self.fetcher)
        runtime.register("RSS", self)
        return launcher.launch(repeater.start)

    def stop(self):
        """ stop rss fetcher. """
        self.kill("RSS")

    def fetcher(self):
        """ find all rss object and fetch the corresponding feeds. """
        from .space import db, seen
        thrs = []
        nr = len(seen.urls)
        for obj in db.find("rss"):
            if "rss" not in obj:
                continue
            if not obj.rss:
                continue
            thr = launcher.launch(self.fetch, obj)
            thrs.append(thr)
        res = launcher.waiter(thrs)
        logging.info("! fetched %s" % ",".join([str(x) for x in res]))
        seen.sync()
        return res

    def synchronize(self):
        """ sync a feed (fetch but don't display). """
        from .space import db, seen
        nr = 0
        for obj in db.find("rss"):
            if not obj.get("rss", None):
                continue
            for o in get_feed(obj.rss):
                if o.link in seen.urls:
                    continue
                seen.urls.append(o.link)
                nr += 1
        logging.info("! synced %s urls" % nr)
        seen.sync()
        return seen

    def fetch(self, obj):
        """ fetch a feed from provied obj (uses obj.rss as the url). """
        from .utils  import file_time, to_time
        from .space import fleet, kernel, seen
        nr = 0
        for o in list(get_feed(obj.rss))[::-1]:
            if o.link in seen.urls:
                continue
            seen.urls.append(o.link)
            feed = Feed(o)
            feed.services = "rss"
            for f in self.cfg.save_list:
                if f in feed.link:
                    if "published" in feed:
                        try:
                            date = file_time(to_time(feed.published))
                            feed.save(stime=date)
                        except botlib.error.ENODATE as ex:
                            logging.info("ENODATE %s" % str(ex))
                    else:
                        feed.save()
            kernel.announce(self.display(feed))
            nr += 1
        return nr

    def display(self, obj):
        """ format feed items so that it can be displayed. """
        result = ""
        for check in self.cfg.descriptions:
            link = obj.get("link", "")
            if check in link:
                summary = obj.get("summary", None)
                if summary:
                    result += "%s - " % summary
        for key in self.cfg.display_list:
            data = obj.get(key, None)
            if data:
                result += "%s - " % data.rstrip()
        if result:
            return result[:-3].rstrip()
