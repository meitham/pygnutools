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
    parser.add_argument('path', action='store', nargs='?', default=os.getcwd())
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('-name', dest='name', action=PrimaryAction)
    parser.add_argument('-true', dest='true', action=PrimaryAction, nargs=0)
    parser.add_argument('-print', dest='print', action=PrimaryAction, nargs='?')
    parser.add_argument('-print0', dest='print0', action=PrimaryAction, nargs=0)
    parser.add_argument('-println', dest='println', action=PrimaryAction, nargs=0)
    parser.add_argument('-print-context', dest='print_context',
            action=PrimaryAction, nargs=0)
    parser.add_argument('-exec', dest='exec', action=PrimaryAction, nargs='+')
    # add plugins
    for plugin in iter_entry_points(group='pygnutools.plugin', name='cli_args'):
        parser = plugin.load()(parser)
    return parser


def main():
    parser = cli_args()
    ns = parser.parse_args()
    tw = TreeWalker(top=ns.path)
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
