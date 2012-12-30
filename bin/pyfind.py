import os
import argparse

from pygnutools import TreeWalker, evaluate


class PrimaryAction(argparse.Action):
    """An Action that collects arguments in the order they appear at the shell
    """
    def __call__(self, parser, namespace, values, option_string=None):
        if not 'primaries' in namespace:
            setattr(namespace, 'primaries', [])
        namespace.primaries.append((self.dest, values))


def parse_args():
    """
    """
    parser = argparse.ArgumentParser(description="extensible pure python "
            "gnu file like tool.")
    parser = argparse.ArgumentParser()
    parser.add_argument('path', action='store', nargs='?', default=os.getcwd())
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('-name', dest='name', action=PrimaryAction)
    parser.add_argument('-make', dest='make', action=PrimaryAction)
    parser.add_argument('-imake', dest='imake', action=PrimaryAction)
    parser.add_argument('-model', dest='model', action=PrimaryAction)
    parser.add_argument('-imodel', dest='imodel', action=PrimaryAction)
    parser.add_argument('-true', dest='true', action=PrimaryAction, nargs=0)
    parser.add_argument('-print', dest='print', action=PrimaryAction, nargs=0)
    parser.add_argument('-print0', dest='print0', action=PrimaryAction, nargs=0)
    parser.add_argument('-print-tag', dest='print_tag', action=PrimaryAction)
    parser.add_argument('-print-all-tags', dest='print_all_tags',
            action=PrimaryAction, nargs=0)
    parser.add_argument('-exec', dest='exec', action=PrimaryAction, nargs='+')
    return parser.parse_args()


def main():
    ns = parse_args()
    tw = TreeWalker(top=ns.path)
    for fpath, fname in tw.walk():
        if not evaluate(fpath, fname, ns):
            continue


if __name__ == '__main__':
    main()
