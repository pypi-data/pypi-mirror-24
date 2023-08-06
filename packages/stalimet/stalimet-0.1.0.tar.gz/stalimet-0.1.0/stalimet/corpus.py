from nltk import AlignedSent

from stalimet.ibm2_exact import IBMModel2Exact


class SentencePair(AlignedSent):
    @property
    def score(self) -> float:
        return self._score

    @score.setter
    def score(self, value: float):
        self._score = value

    def __init__(self, words, mots, alignment=None):
        super(SentencePair, self).__init__(words, mots, alignment=alignment)
        self._score = 0.0

    def __str__(self):
        return str(self.score) + ' ||| ' + ' '.join(self.words) + ' ||| ' + ' '.join(self.mots)

    def align(self, model: IBMModel2Exact):
        model.align(self)


class ParallelCorpus(list):
    @property
    def alignment_model(self) -> IBMModel2Exact:
        return self._alignment_model

    @alignment_model.setter
    def alignment_model(self, model: IBMModel2Exact):
        self._alignment_model = model

    def __init__(self):
        super(ParallelCorpus, self).__init__()
        self._alignment_model = None
        self._self_trained  = False

    def build_parallel_corpus(self, tgt: list, ref: list) -> 'ParallelCorpus':
        for i in range(len(tgt)):
            self.append(SentencePair(tgt[i].split(), ref[i].split()))
        return self

    def train_alignment_model(self):
        self._alignment_model = IBMModel2Exact(self, 5)
        return self

    def align_sentences(self):
        if not self._self_trained:
            for sentence_page in self:
                self.alignment_model.align(sentence_page)

