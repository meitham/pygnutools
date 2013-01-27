import os
import argparse

from pygnutools import TreeWalker, evaluate

from pkg_resources import iter_entry_points


class PrimaryAction(argparse.Action):
    """An Action that collects arguments in the order they appear at the shell
    """
    def __call__(self, parser, namespace, values, option_string=None):
        if not 'primaries' in namespace:
            setattr(namespace, 'primaries', [])
        namespace.primaries.append((self.dest, values))


def cli_args():
    """
    """
    parser = argparse.ArgumentParser(description="extensible pure python "
            "gnu file like tool.")
    parser = argparse.ArgumentParser()
    parser.add_argument('-follow', dest='follow_links', action='store_true',
            help="""Follow symbolic links, the default is not to follow.""",
            default=False)
    parser.add_argument('-depth', '-d', dest='depth_first',
            action='store_true', default=False,
            help="""Process the subdirectory before processing the sibling
            files available under that directory.
            """)
    parser.add_argument('-maxdepth', dest='max_depth',
            action='store', default=None, type=int, nargs=1,
            help="""Limit the recursion to a maximum depth. The default is
            unlimited depth.
            """)
    parser.add_argument('path', action='store', nargs='?', default=os.getcwd(),
            help="""The root of the processing tree, this defaults to the
            current working directory `pwd`.""")
    parser.add_argument('--verbose', '-v', action='count', help="""
            The level of verbosirty. The more v you add the more stuff you will
            see.
            """)
    parser.add_argument('-name', dest='name', action=PrimaryAction,
            help="""Match by filename, accepts UNIX globbing patterns.
            e.g. `-name *.rst`
            """)
    parser.add_argument('-iname', dest='iname', action=PrimaryAction,
            help="""Match by filename, similar to `-name` but this is case
            insensitive match.
            """)
    parser.add_argument('-true', dest='true', action=PrimaryAction, nargs=0,
            help="""Always evaluates to True""")
    parser.add_argument('-false', dest='false', action=PrimaryAction, nargs=0,
            help="""Always evaluates to False""")
    parser.add_argument('-print', dest='print', action=PrimaryAction, nargs='?',
            help="""Prints the file path. It accepts an optional argument as
            a string which is used as a seperator, e.g. `-print ','` would
            print the file path followed by a comma, thus any further print
            from thie file context would be printed on the same line after the
            comma. Each file is printed in a new line so this should not be
            confused as a separator between matching files.""")
    parser.add_argument('-print0', dest='print0', action=PrimaryAction, nargs=0,
            help="""Print the file path follows by a null character rather than
            space. Helpful to be used with `xargs -0`.""")
    parser.add_argument('-println', dest='println', action=PrimaryAction,
            nargs=0, help="""Print the file path followed by a new line.
            """)
    parser.add_argument('-print-context', dest='print_context',
            action=PrimaryAction, nargs=0, help=""""
            Prints the context for the match, the context is implemented as a
            mapping object where primaries can add/remove/modify any of the
            key/value pairs.""")
    parser.add_argument('-exec', dest='exec', action=PrimaryAction, nargs='+',
            help="""Execute a shell command when a match happens, any `{}` will
            be replaced by the match path.""")
    # add plugins
    for plugin in iter_entry_points(group='pygnutools.plugin', name='cli_args'):
        parser = plugin.load()(parser)
    return parser


def main():
    parser = cli_args()
    ns = parser.parse_args()
    tw = TreeWalker(top=ns.path, **ns.__dict__)
    from pygnutools import primaries_map
    primaries = getattr(ns, 'primaries', [])
    if not primaries:
        primaries = [('print', None)]
    # add plugins
    for plugin in iter_entry_points(group='pygnutools.plugin',
            name='primaries'):
        primaries_map.update(plugin.load())
    for dirname, filename in tw.walk():
        evaluate(dirname, filename, primaries, ns.verbose)
