"""These are simple callables that correspond to ``find`` primaries. Each
callable takes a context and return the context. The primary would be a failure
if it return anything other than a context. A context is any mapping.
"""

from __future__ import print_function

import fnmatch
import os
import subprocess
import pprint

from .core import Primary


class NameMatchPrimary(Primary):
    """Compares a file name against a pattern
    similar to `find -name arg1`
    """
    def __call__(self, context):
        filename = context['filename']
        pattern = context['args']
        if fnmatch.fnmatch(filename, pattern):
            return context


class PrintPrimary(Primary):
    """Prints out the filename
    similar to `find . -print`
    """
    def __call__(self, context):
        path = context['path']
        suffix = context['args']
        context['buffer'].append(path)
        if suffix:
            context['buffer'].append(suffix)
            return context
        if getattr(self, 'null', False):
            context['buffer'].append('\x00')
        return context


class PrintLineFeedPrimary(Primary):
    """Prints out a new line
    Useful to separate outputs into several lines
    """
    def __call__(self, context):
        context['buffer'].append('\n')
        return context


class PrintContext(Primary):
    """Prints out the conext
    Useful for debugging
    """
    def __call__(self, context):
        context['buffer'].append(pprint.pformat(context))
        return context


class ExecPrimary(Primary):
    """Calls an external command, inspired by find -exec
    {} will be converted to file path anywhere it appears in the args.
    TODO: added context params inside {}
    """
    def __call__(self, context):
        path = context['path']
        command = context['args']
        command = [path if t == '{}' else t for t in command]
        subprocess.call(command[:-1])
        return context


primaries_map = {
        'name': NameMatchPrimary(),
        'print': PrintPrimary(),
        'println': PrintLineFeedPrimary(),
        'print0': PrintPrimary(null=True),
        'print_context': PrintContext(),
        'exec': ExecPrimary(),
}
