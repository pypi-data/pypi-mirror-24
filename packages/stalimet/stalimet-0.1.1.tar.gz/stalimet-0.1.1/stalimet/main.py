from stalimet.corpus import ParallelCorpus
from stalimet.preprocess import run_preprocess
from stalimet.score import Scorer


class Stalimet:
    """
    Main metric class encapsulating training, aligning and scoring the parallel corpora of translation / reference
    segments, if extrenal train corpus is proved the alignment model is trained using this corpus,
    if not it is trained on the corpus for scoring
    """

    @property
    def train_corpus(self) -> ParallelCorpus:
        return self._train_corpus

    @property
    def corpus(self) -> ParallelCorpus:
        return self._corpus

    @property
    def language(self) -> str:
        return self._language

    def __init__(self, tgt_path: str, ref_path: str,
                 tgt_train_path: str = None, ref_train_path: str = None, language: str = 'english'):
        self._language = language
        self._corpus = ParallelCorpus()
        self._tgt_path = tgt_path
        self._ref_path = ref_path

        if not (tgt_train_path is None or ref_train_path is None):
            self._train_corpus = ParallelCorpus()
            self._tgt_train_path = tgt_train_path
            self._ref_train_path = ref_train_path
        else:
            self._train_corpus = None

    def train(self, keep_punctuation=False):
        tgt = run_preprocess(self._tgt_path, self._language, keep_punctuation)
        ref = run_preprocess(self._ref_path, self._language, keep_punctuation)
        self._corpus.build_parallel_corpus(tgt, ref)

        # if train corpus is specified we train alignment model on it and pass to main corpus,
        # if not train it on main corpus
        if self._train_corpus is not None:
            tgt_train = run_preprocess(self._tgt_train_path, self._language)
            ref_train = run_preprocess(self._ref_train_path, self._language)
            self._train_corpus.build_parallel_corpus(tgt_train, ref_train)
            self._train_corpus.train_alignment_model()
            self._corpus.alignment_model = self._train_corpus.alignment_model
        else:
            self._corpus.train_alignment_model()

        self._corpus.align_sentences()

    def score(self) -> list:
        scorer = Scorer(self._corpus)
        scorer.calculate_scores()

        scores = []
        for entry in self._corpus:
            scores.append(entry.score)

        return scores
