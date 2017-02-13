#!/usr/bin/env python
from argparse import ArgumentParser
import os
import markovator as mk


def readFile(filename):
    with open(filename, 'r') as f:
        return f.read()


def writeFile(filename, data):
    with open(filename, 'w') as f:
        f.write(data)


def getParser():
    parser = ArgumentParser()
    parser.add_argument('sources', nargs='+', metavar='SRC/')
    parser.add_argument('-p', '--posified', dest='posified', action='store_true')
    parser.add_argument('-n', '--newline', dest='newline', action='store_true')
    parser.add_argument('-d', '--dest', metavar='DEST')
    parser.add_argument('-m', '--mix', metavar='LIST')
    return parser


def loadModel(filename, is_posified, is_newline):
    mkvtr = mk.Markovator()
    mkvtr.set_method(is_posified, is_newline)
    mkvtr.process_model_from_input(readFile(filename))
    print('Model "{}" loaded.'.format(filename))
    return mkvtr


def saveModel(filename, mkvtr):
    processed_model = mkvtr.process_model_for_output()
    writeFile(filename, processed_model)
    print('Model "{}" written to disk.'.format(filename))


def combineModels(filenames, ratios, options):
    models = [loadModel(os.path.expanduser(os.path.expandvars(filename)), *options).model for filename in filenames]
    mkvtr = mk.Markovator()
    mkvtr.set_model(mkvtr.combine_models(models, ratios))
    print('Models "{}" combined at {}'.format(filenames, ratios))
    return mkvtr


def main():
    args = getParser().parse_args()
    if args.dest:
        out_name = os.path.expanduser(os.path.expandvars(args.dest))
    else:
        out_name = './c_'+'_'.join(args.sources)
    combined_model = combineModels(args.sources, [int(x) for x in args.mix.split(',')], (args.posified, args.newline))
    saveModel(out_name, combined_model)


if __name__ == '__main__':
    main()

