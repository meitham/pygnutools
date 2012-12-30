"""These are simple callables that correspond to ``find`` primaries. Each
callable takes a context and return the context. The primary would be a failure
if it return anything other than a context. A context is any mapping.
"""

from __future__ import print_function

import fnmatch
import os
import subprocess

from .core import Primary


class NameMatchPrimary(Primary):
    """Compares a file name against a pattern
    similar to `find -name arg1`
    """
    def __call__(self, context):
        fname = context['fname']
        pattern = context['args']
        if fnmatch.fnmatch(fname, pattern):
            return context


class PrintPrimary(Primary):
    """Prints out the filename
    similar to `find . -print`
    """
    def __call__(self, context):
        fpath = context['fpath']
        fname = context['fname']
        if getattr(self, 'null', False):
            print(os.path.join(fpath, fname), end='\x00')
        else:
            print(os.path.join(fpath, fname))


class ExecPrimary(Primary):
    """
    """
    def __call__(self, context):
        fpath = context['fpath']
        fname = context['fname']
        path = os.path.join(fpath, fname)
        command = context['args']
        command = [path if t == '{}' else t for t in command]
        #print(' '.join(command))
        subprocess.call(command[:-1])


primaries_map = {
        'name': NameMatchPrimary(),
        'print': PrintPrimary(),
        'print0': PrintPrimary(null=True),
        'exec': ExecPrimary(),
}
