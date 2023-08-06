import os

with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as f:
    __version__ = f.read().strip()
__author__ = 'Daniel Nyga'

from .debug import out, stop, trace, stoptrace
from .tools import ifnone, ifnot, allnone, allnot, edict, idxif, first, last
from .signals import add_handler, rm_handler, enable_ctrlc
from .threads import Lock, RLock, Condition, Event, Semaphore, BoundedSemaphore, Barrier, Relay, Thread, \
    SuspendableThread
from .logs import loggers, newlogger, getlogger, DEBUG, INFO, WARNING, ERROR, CRITICAL, expose, inspect, active_exposures
from .console import ProgressBar, StatusMsg, bf

enable_ctrlc()