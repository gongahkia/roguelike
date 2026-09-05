import argparse

from main import rungame


def parseargs ():
    parser = argparse.ArgumentParser(description = 'Play the terminal roguelike.')
    parser.add_argument('--level',choices = ['0','1','2','3','boss'],help = 'Start a level directly for debugging.')
    return parser.parse_args()


def main ():
    arguments = parseargs()
    if arguments.level is None:
        rungame()
        return
    if arguments.level == 'boss':
        rungame(3)
        return
    rungame(int(arguments.level))


if __name__ == '__main__':
    main()
