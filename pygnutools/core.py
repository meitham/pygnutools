import os
import traceback

try:
    import ipdb as pdb
except ImportError:
    import pdb

from pkg_resources import iter_entry_points


class Primary(object):
    """This will be extended by all primaries
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def evaluate(dirname, filename, primaries, verbosity):
    """Evaluates a user test and return True or False, like GNU find tests
    """
    from pygnutools import primaries_map
    context = {
            'dirname': dirname,
            'filename': filename,
            'path': os.path.join(dirname, filename),
            'verbosity': verbosity,
            'buffer': [],
    }
    for primary, args in primaries:
        context.update({'args': args})
        primary_object = primaries_map[primary]
        context = primary_object(context)
        if not context:
            return False
    line = ''.join(context['buffer'])
    if line.strip():
        print(line)
    else:  # do what find does - print the path
        print(context['path'])
    return True


class TreeWalker(object):
    """provides a functionality similar to os.walk but can do
    pre defined depth when needed.
    """
    def __init__(self, *args, **kwargs):
        self._top = kwargs.get('top', os.getcwd())
        self._max_depth = kwargs.get('max_depth')
        self.depth_first = kwargs.get('depth_first', False)
        self._depth = 0
        if self._max_depth is None or self._max_depth > 0:
            self._recursive = True
        else:
            self._recursive = False
        self._follow_links = kwargs.get('follow_links', False)

    def __repr__(self):
        return 'TreeWalker(top=%(_top)s, max_depth=%(_max_depth)r)' % locals()

    def walk(self, top=None, depth=0):
        if not top:
            top = self._top
        if self._max_depth is not None:
            if depth > self._max_depth:
                return
        if os.path.isdir(top):
            for f in sorted(os.listdir(top), key=os.path.isdir,
                    reverse=self.depth_first):
                file_path = os.path.join(top, f)
                if os.path.isdir(file_path) and self._recursive:
                    islink = os.path.islink(file_path)
                    if islink and not self._follow_links:
                        continue
                    for d, f in self.walk(file_path, depth+1):
                        yield d, f
                elif os.path.isfile(file_path):
                    yield top, f
        else:
            yield os.path.split(top)
