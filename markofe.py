#!/usr/bin/env python
import markovator as mk
from argparse import ArgumentParser
import os


def loadTextFile(filename):
    with open(filename, 'r') as f:
        return f.read()


def getArgParser():
    parser = ArgumentParser(description='Parse some text (or use a pre-generated model) using markovify to generate sentences.')
    parser.add_argument('-n', '--newline',
                        action='store_true',
                        help='Indicates that texts have newline delimited sentences.')
    parser.add_argument('-p', '--posify',
                        dest='pos',
                        action='store_true',
                        help='Indicates that corpus should be analyzed using nltk\'s part-of-speech tagging.')
    parser.add_argument('-m', '--model',
                        dest='model',
                        metavar='PATH_TO_MODEL/',
                        default=None,
                        help='Indicates a model to use to generate sentences.')
    parser.add_argument('-o', '--out',
                        dest='out',
                        metavar='OUTPUT_DEST/',
                        default=None,
                        help='Indicates that the model generated should be output to the indicated filename.')
    parser.add_argument('-s', '--source',
                        dest='source',
                        metavar='PATH_TO_FILES/',
                        default='./',
                        help='If generating a model, indicates the directory where the texts reside. [./]')
    parser.add_argument('--num',
                        metavar='INT',
                        type=int,
                        default=1,
                        help='Indicates the number of sentences to generate. [1]')
    parser.add_argument('--chars',
                        metavar='INT',
                        type=int,
                        default=0,
                        help='Indicates the max characters to generate for each sentence. [0=unlimited]')
    parser.add_argument('--state_size',
                        metavar='INT',
                        type=int,
                        default=2,
                        help='Indicates the state size to be used when generating the model. [2]')
    parser.add_argument('--max_overlap_ratio',
                        metavar='FLOAT',
                        type=float,
                        default=0.7,
                        help='Indicates the max_overlap_ratio of the generated sentences (see markovify docs for more \
                            info). [None=default]')
    parser.add_argument('--max_overlap_total',
                        metavar='INT',
                        type=int,
                        default=15,
                        help='Indicates the max_overlap_total of the generated sentences (see markovify docs for more \
                            info). [None=default]')
    # parser.add_argument('-c', '--config', dest='config_file', default=None,
    #                   help='Path to a config file to load. Any conflicting arguments supplied will resolve in the \
    #                       config file's favor.)
    return parser


def compileTexts(source_dir):
    corpus = ''
    for filename in [os.path.join(x[0], y) for x in os.walk(source_dir) for y in x[2]]:
        with open(filename) as text:
            corpus += ' '+text.read()
            print('Compiling {} ...'.format(filename))
    return corpus.decode('utf-8')


def processCorpus(args):
    mkvtr = mk.Markovator()
    mkvtr.set_method(args.pos, args.newline)
    if args.model:
        mkvtr.process_model_from_input(loadTextFile(args.model))
    else:
        mkvtr.set_corpus(compileTexts(args.source))
        mkvtr.generate_model(state_size=args.state_size)
    if args.out:
        with open(args.out, 'w') as f:
            f.write(mkvtr.process_model_for_output())
    sentences = mkvtr.markovate_sentences(args.num, args.chars, max_overlap_ratio=args.max_overlap_ratio, max_overlap_total=args.max_overlap_total)
    print sentences.encode('utf-8')


def main():
    args = getArgParser().parse_args()
    processCorpus(args)


if __name__ == '__main__':
    main()
