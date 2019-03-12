# -*- coding: utf-8 -*-

VERSION = (0, 0, 0)
__version__ = ".".join(map(str, VERSION[0:3])) + "".join(VERSION[3:])
__license__ = "BSD"

from poorscrum.poorscrum_config import *
from poorscrum.poorscrum_story import *
from poorscrum.poorscrum_tasks import *
from poorscrum.poorscrum_tools import *
