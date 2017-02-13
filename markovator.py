from functools import partial
import pMarko as pmk

class Markovator(object):

    def __init__(self):
        self.method = None
        self.corpus = None
        self.model = None

    def generate_model(self, s=None, **kwargs):
        if s:
            self.model = self.method(s, **kwargs)
        else:
            self.model = self.method(self.corpus, **kwargs)
        return self.model

    def set_corpus(self, text_file):
        self.corpus = text_file

    def set_model(self, model):
        self.model = model

    def set_method(self, is_posified, is_newline):
        if is_posified and is_newline:
            self.method = pmk.POSifiedNewlineText
        elif is_posified:
            self.method = pmk.POSifiedText
        elif is_newline:
            self.method = pmk.NewlineText
        else:
            self.method = pmk.Text

    def markovate_sentences(self, number_of_sentences=1, sentence_length=0, **kwargs):
        sentencer = self._strangeMethod(sentence_length)
        sentences = []
        for item in range(number_of_sentences):
            generated_sentence = sentencer(**kwargs)
            if generated_sentence:
                sentences.append(generated_sentence)
            # else:
            #     print("Skipped a sentence!")
        output = "\n".join(sentences)
        return output

    def _strangeMethod(self, length):
        if length == 0:
            output_func = self.model.make_sentence
        else:
            output_func = partial(self.model.make_short_sentence, length)
        return output_func

    def process_model_for_output(self):
        output_json = None
        if self.model is not None:
            output_json = self.model.to_json()
        return output_json

    def process_model_from_input(self, input_json):
        self.model = self.method.from_json(input_json)

    def combine_models(self, sources, ratios):
        model_combo = pmk.combine(sources, ratios)
        return model_combo
