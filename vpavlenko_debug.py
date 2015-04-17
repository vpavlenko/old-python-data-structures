#!/usr/bin/env python3

import colorama
colorama.init()

from sys import stderr

import functools

level = 0


def to_string(s):
    s = str(s) if not isinstance(s, str) else s.encode("utf-8")
    if len(s) > 100:
        s = s[:50] + ' ...' + s[-50:]
    return s


def debug_color(func):
    @functools.wraps(func)
    def debug_wrapper(*args, **kwargs):
        global level
        funcname_color = colorama.Fore.GREEN
        par_color = colorama.Fore.BLUE
        value_color = colorama.Fore.RED
        indent = '    ' * level
        func_str = func.__name__
        args_list = [value_color + to_string(s) + par_color for s in args]
        kwargs_list = ['%s=%s%s%s' % (k, value_color, to_string(kwargs[k]), par_color) for k in kwargs]
        print(funcname_color + '%s%s%s(%s)' % (indent, func_str, par_color, ', '.join(args_list + kwargs_list)) + colorama.Fore.RESET, file=stderr)
        level += 1
        retval = func(*args, **kwargs)
        print('%s= %s' % (indent, to_string(retval)))
        level -= 1
        return retval

    return debug_wrapper
        

def debug_calls_limit(num_calls):
    def decorator(func):
        class CallLimitExceeded:
            
            def __repr__(self):
                return 'CallLimitExceeded'
            
            def __bool__(self):
                return False
            
        cle = CallLimitExceeded()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if wrapper.calls_remain > 0:
                wrapper.calls_remain -= 1
                return func(*args, **kwargs)
            else:
                return cle

        wrapper.calls_remain = num_calls
        return wrapper

    return decorator


if __name__ == '__main__':
    @debug_color
    @debug_calls_limit(3)
    def rec(level):
        if level > 0:
            rec(level - 1)

    rec(10)
