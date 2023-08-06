import sys
is_py3 = sys.version_info[0] >= 3

if is_py3:
    string_type = str  # noqa
    all_string_types = [str]
    from functools import singledispatch, lru_cache
else:
    string_type = basestring  # noqa
    all_string_types = [basestring, str, unicode]
    from singledispatch import singledispatch
    from functools32 import lru_cache
