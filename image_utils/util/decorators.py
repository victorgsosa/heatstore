import functools
import logging
import time


def lazy_property(function):
    attribute = '_cache_' + function.__name__

    @property
    @functools.wraps(function)
    def decorator(self):
        if not hasattr(self, attribute):
            setattr(self, attribute, function(self))
        return getattr(self, attribute)

    return decorator

def timing(function):
	log = logging.getLogger(function.__module__)
	def wrap(*args):
		time1 = time.time()
		ret = function(*args)
		time2 = time.time()
		log.info('%s function took %0.3f ms', function.__name__, (time2-time1)*1000.0)
		return ret
	return wrap