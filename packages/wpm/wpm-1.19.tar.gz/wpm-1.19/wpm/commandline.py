import argparse
import codecs
import pkg_resources
import sys
import urwid
import wpm
import wpm.game

def parse_args():
    p = argparse.ArgumentParser(prog="wpm", epilog=wpm.__copyright__)

    p.add_argument("--load-json", metavar="FILENAME", default=None,
            help="""JSON file containing texts to train on.

The format is

[{"author": "...", "title": "...", "text": "..."}, ...]
""")
    p.add_argument("--load", metavar="FILENAME", default=None,
            help="A pure text file to train on.")

    p.add_argument("-V", "--version", default=False, action="store_true",
            help="Show program version")

    p.add_argument("--tab", default=None, type=int,
            help="If set, expand tabs to this number of spaces")

    opts = p.parse_args()

    if opts.version:
        print("WPM v%s" % wpm.__version__)
        print(wpm.__copyright__)
        print("Distributed under the %s" % wpm.__license__)
        sys.exit(0)

    return opts

def main():
    opts = parse_args()
    texts = []

    if opts.load_json is not None:
        texts += wpm.game.load(opts.load_json)

    if opts.load is not None:
        with codecs.open(opts.load, encoding="utf-8") as f:
            text = f.read().replace("\r", "").rstrip()
        texts.append({"author": "", "title": "", "text": text})

    if len(texts) == 0:
        filename = pkg_resources.resource_filename("wpm", "data/examples.json")
        texts = wpm.game.load(filename)

    try:
        game = wpm.game.Game(texts)
        game.set_tab_spaces(opts.tab)
        game.run()
    except urwid.main_loop.ExitMainLoop:
        pass
