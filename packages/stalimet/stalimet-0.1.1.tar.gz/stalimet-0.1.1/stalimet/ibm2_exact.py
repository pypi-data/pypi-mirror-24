from nltk.translate.ibm2 import IBMModel2, IBMModel
from nltk.translate import Alignment


class IBMModel2Exact(IBMModel2):
    """
    Modifies imb1 lexical translation model by giving maximum
    probability to exact matching words
    """

    def __init__(self, sentence_aligned_corpus, iterations, probability_tables=None):
        super(IBMModel2, self).__init__(sentence_aligned_corpus)

        if probability_tables is None:
            self.set_uniform_probabilities(sentence_aligned_corpus)
        else:
            # Set user-defined probabilities
            self.translation_table = probability_tables['translation_table']

        for n in range(0, iterations):
            self.train(sentence_aligned_corpus)

        self.__align_all(sentence_aligned_corpus)

    def __align_all(self, parallel_corpus):
        for sentence_pair in parallel_corpus:
            self.__align(sentence_pair)

    def __align(self, sentence_pair):
        """
        Determines the best word alignment for one sentence pair from
        the corpus that the model was trained on.

        The best alignment will be set in ``sentence_pair`` when the
        method returns. In contrast with the internal implementation of
        IBM models, the word indices in the ``Alignment`` are zero-
        indexed, not one-indexed.

        :param sentence_pair: A sentence in the source language and its
            counterpart sentence in the target language
        :type sentence_pair: AlignedSent
        """
        best_alignment = []

        for j, trg_word in enumerate(sentence_pair.words):
            # Initialize trg_word to align with the NULL token
            best_prob = max(self.translation_table[trg_word][None],
                            IBMModel.MIN_PROB)
            best_alignment_point = None
            for i, src_word in enumerate(sentence_pair.mots):
                align_prob = self.translation_table[trg_word][src_word]
                if trg_word == src_word:
                    align_prob = 1
                if align_prob >= best_prob:  # prefer newer word in case of tie
                    best_prob = align_prob
                    best_alignment_point = i

            best_alignment.append((j, best_alignment_point))

        sentence_pair.alignment = Alignment(best_alignment)

    def align(self, sentence_pair):
        self.__align(sentence_pair)