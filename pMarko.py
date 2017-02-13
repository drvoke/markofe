from markovify import *
from re import split as resplit
from nltk.tag.perceptron import PerceptronTagger

tagger = PerceptronTagger()

def joinWords(tag, debug=False):
    output = "::".join(tag)
    if debug:
        print("<{}>".format(output.encode("utf-8")))
    return output


class POSifiedText(Text):
    def word_split(self, sentence):
        words = resplit(self.word_split_pattern, sentence)
        words = [word for word in words if len(word) > 0]
        words = [joinWords(tag) for tag in tagger.tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


class POSifiedNewlineText(POSifiedText):
    def sentence_split(self, text):
        return resplit(r"\s*\n\s*", text)
