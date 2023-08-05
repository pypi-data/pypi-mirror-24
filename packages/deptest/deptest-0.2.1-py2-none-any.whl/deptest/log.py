# coding: utf-8

import sys
import curses
import logging
import threading
from .utils import anyp, unicode_type, to_unicode

lg = logging.getLogger('deptest.log')


def setup_log_handler(log_handler, clear=False):
    # setup our handler with root logger
    root_logger = logging.getLogger()
    if clear:
        if hasattr(root_logger, "handlers"):
            for handler in root_logger.handlers:
                root_logger.removeHandler(handler)
        for logger in logging.Logger.manager.loggerDict.values():
            if hasattr(logger, "handlers"):
                for handler in logger.handlers:
                    logger.removeHandler(handler)
    # make sure there isn't one already
    # you can't simply use "if log_handler not in root_logger.handlers"
    # since at least in unit tests this doesn't work --
    # LogCapture() is instantiated for each test case while root_logger
    # is module global
    # so we always add new MyMemoryHandler instance
    for handler in root_logger.handlers[:]:
        if isinstance(handler, MyMemoryHandler):
            root_logger.handlers.remove(handler)
    root_logger.addHandler(log_handler)
    lg.debug('root logger handlers: %s', root_logger.handlers)
    # to make sure everything gets captured
    loglevel = "NOTSET"
    root_logger.setLevel(getattr(logging, loglevel))


def set_logger(name,
               level=logging.INFO,
               fmt='%(name)s %(levelname)s %(message)s',
               propagate=1):
    """
    This function will clear the previous handlers and set only one handler,
    which will only be StreamHandler for the logger.

    This function is designed to be able to called multiple times in a context.

    Note that if a logger has no handlers, it will be added a handler automatically when it is used.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = propagate

    handler = None
    for h in logger.handlers:
        if isinstance(h, logging.StreamHandler):
            # use existing instead of clean and create
            handler = h
            break
    if not handler:
        handler = logging.StreamHandler()
        logger.addHandler(handler)

    handler.setFormatter(logging.Formatter(fmt=fmt))


class MyMemoryHandler(logging.Handler):
    def __init__(self, logformat, logdatefmt=None, filters=None):
        logging.Handler.__init__(self)
        fmt = logging.Formatter(logformat, logdatefmt)
        self.setFormatter(fmt)
        if filters is None:
            filters = ['-deptest']
        self.filterset = FilterSet(filters)
        self.buffer = []

    def emit(self, record):
        self.buffer.append(self.format(record))

    def flush(self):
        pass

    def truncate(self):
        self.buffer = []

    def filter(self, record):
        if self.filterset.allow(record.name):
            return logging.Handler.filter(self, record)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.RLock()


class FilterSet(object):
    def __init__(self, filter_components):
        self.inclusive, self.exclusive = self._partition(filter_components)

    # @staticmethod
    def _partition(components):
        inclusive, exclusive = [], []
        for component in components:
            if component.startswith('-'):
                exclusive.append(component[1:])
            else:
                inclusive.append(component)
        return inclusive, exclusive
    _partition = staticmethod(_partition)

    def allow(self, record):
        """returns whether this record should be printed"""
        if not self:
            # nothing to filter
            return True
        return self._allow(record) and not self._deny(record)

    # @staticmethod
    def _any_match(matchers, record):
        """return the bool of whether `record` starts with
        any item in `matchers`"""
        def record_matches_key(key):
            return record == key or record.startswith(key + '.')
        return anyp(bool, map(record_matches_key, matchers))
    _any_match = staticmethod(_any_match)

    def _allow(self, record):
        if not self.inclusive:
            return True
        return self._any_match(self.inclusive, record)

    def _deny(self, record):
        if not self.exclusive:
            return False
        return self._any_match(self.exclusive, record)


class Color(object):
    DEFAULT_COLORS = {
        'blue': 4,
        'green': 2,
        'yellow': 3,
        'red': 1,
    }

    def __init__(self, colors=DEFAULT_COLORS):
        enable = False
        if curses and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            try:
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    enable = True
            except Exception:
                pass

        self._colors = {}

        if enable:
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = unicode_type(fg_color, "ascii")

            for name, code in colors.items():
                self._colors[name] = unicode_type(curses.tparm(fg_color, code), "ascii")
            self._normal = unicode_type(curses.tigetstr("sgr0"), "ascii")
        else:
            self._normal = ''

        self.enable = enable

    def dye(self, name, s):
        if name in self._colors:
            start = self._colors[name]
        else:
            start = self._normal
        end = self._normal
        ctx = {'start': start, 'end': end, 'content': to_unicode(s)}
        us = u'%(start)s%(content)s%(end)s' % ctx
        return us.encode('utf8')

color = Color()
