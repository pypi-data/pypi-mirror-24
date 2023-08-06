from stalimet.corpus import ParallelCorpus, SentencePair


class Scorer(object):

    def __init__(self, corpus: ParallelCorpus):
        self._corpus = corpus

    @staticmethod
    def __count_chunks(sentence_pair: SentencePair) -> int:
        previous_index = -1
        chunks = 1
        for a in sorted(sentence_pair.alignment):
            if previous_index != -1 and (a[1] is None or previous_index != a[1] - 1):
                chunks += 1
            previous_index = a[1]

        return chunks

    @staticmethod
    def __count_matching_chars(word1: str, word2: str) -> int:
        count = 0
        for i, c in enumerate(word1):
            if len(word2) > i and c == word2[i]:
                count += 1

        return count

    @staticmethod
    def __calculate_char_match(sentence_pair: SentencePair) -> float:
        matches = 0.0
        for a in sorted(sentence_pair.alignment):
            count = 0 if a[1] is None else Scorer.__count_matching_chars(sentence_pair.words[a[0]], sentence_pair.mots[a[1]])
            if count > 0:
                matches += count / len(sentence_pair.words[a[0]])
        return matches

    def calculate_scores(self):
        """
        calculates scores for every sentence of the corpus using the formula:

        score = (sum(matching_character_for_every_word) / number_of_words) * fragmentation_penalty
        fragmentation_penalty = number_of_continuous_chunks / (2 * sum(matching_character_for_every_word))

        and stores the score in the sentence pair class
        """
        for i, sentence_pair in enumerate(self._corpus):
            try:
                chunks = Scorer.__count_chunks(sentence_pair)
                match = Scorer.__calculate_char_match(sentence_pair)

                recall = match / len(sentence_pair.mots)
                penalty = 0 if chunks == 1 else 0.5 * float(chunks) / match

                score = recall * (1.0 - penalty)
            except ZeroDivisionError:
                score = 0

            sentence_pair.score = score
