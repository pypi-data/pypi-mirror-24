from nltk.tokenize import word_tokenize
import string


def run_preprocess(path, language, keep_punctuation=False):
    preprocess = Preprocess(open(path).readlines(), language).lowercase().tokenize()
    if not keep_punctuation:
        preprocess = preprocess.remove_punctuation()
    return preprocess.lines


class Preprocess:

    def __init__(self, lines: list, language: str):
        self.lines = [line.strip() for line in lines]
        self.preprocessor_run = []
        self.language = language

    def lowercase(self) -> 'Preprocess':
        for i, line in enumerate(self.lines):
            self.lines[i] = self.lines[i].lower()
        return self

    def remove_punctuation(self) -> 'Preprocess':
        translate_table = dict((ord(char), None) for char in string.punctuation)
        for i, line in enumerate(self.lines):
            self.lines[i] = self.lines[i].translate(translate_table)
        return self

    def tokenize(self) -> 'Preprocess':
        for i, line in enumerate(self.lines):
            self.lines[i] = ' '.join(word_tokenize(self.lines[i], self.language))
        return self

    def split(self) -> 'Preprocess':
        for i, line in enumerate(self.lines):
            self.lines[i] = self.lines[i].split()
        return self
