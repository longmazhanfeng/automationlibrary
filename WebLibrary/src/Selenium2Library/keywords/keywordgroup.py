import sys
import inspect
import re

try:
    from decorator import decorator
except SyntaxError: # decorator module requires Python/Jython 2.4+
    decorator = None
if sys.platform == 'cli':
    decorator = None # decorator module doesn't work with IronPython 2.6

def _run_on_failure_decorator(method, *args, **kwargs):
    self = args[0]
    already_in_keyword = getattr(self, "_already_in_keyword", False) # If False, we are in the outermost keyword (or in `run_keyword`, if it's a dynamic library)
    self._already_in_keyword = True # Set a flag on the instance so that as we call keywords inside this call and this gets run again, we know we're at least one level in.
    
    try:
        # If _web_gen_gif(_webkeywords) is setted True, capture the Screen when users do actions(Click/Input/Choose/Upload/Get)
        if self._web_gen_gif == True:
            if(re.search(r'[Cc]lick|[Ii]nput|[Cc]hoose|[Uu]pload|[Gg]et',method.__name__)):
                self.capture_page_screenshot_without_html_log()
        return method(*args, **kwargs)

    except Exception, err:
        if hasattr(self, '_run_on_failure') and not self._has_run_on_failure:
            # If we're in an inner keyword, track the fact that we've already run on failure once
            self._has_run_on_failure = True
            self._run_on_failure()
        raise
    finally:
        if not already_in_keyword:
            # If we are in the outer call, reset the flags.
            self._already_in_keyword = False
            self._has_run_on_failure = False

class KeywordGroupMetaClass(type):
    def __new__(cls, clsname, bases, dict):
        if decorator:
            for name, method in dict.items():
                if not name.startswith('_') and inspect.isroutine(method):
                    dict[name] = decorator(_run_on_failure_decorator, method)
        return type.__new__(cls, clsname, bases, dict)

class KeywordGroup(object):
    __metaclass__ = KeywordGroupMetaClass
