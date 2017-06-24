
from collections import defaultdict
from itertools import tee
from random import choice
import re
from nltk.tokenize import sent_tokenize


def nwise(iterable, n=2):
    """nwise([1, 2, 3, 4], n=3) => [(1, 2, 3), (2, 3, 4)]"""
    if len(iterable) < n:
        return
    iterables = tee(iterable, n)
    for i, iter_ in enumerate(iterables):
        for num in range(i):
            next(iter_)
    return zip(*iterables)


class Markovizer(object):
    """
    Creates a markov chain sentence from a given text.
    Parameters
    ----------
    input : string, '' is default.
        If input is a file path, the text to train the markovizer will
        be drawn from that file.
        Otherwise the input is expected to be a text string that
        that markovizer will use to construct the probability
        distribution.
    encoding : string, 'utf-8' is default.
        The encoding will be the encoding used to open the file,
        if input is a file path.
    token_pattern : raw string
        The pattern to use to find the tokens in the intial sentence.
    """
    def __init__(self, text, encoding='utf-8',
                 token_pattern=r'\w+|[^\w\s]'):
        try:
            with open(text, encoding=encoding) as f:
                self.text = f.read()
        except FileNotFoundError:
            self.text = text
        self.token_pattern = token_pattern
        self.prob_dist = None
        self.utterance = None
        # new seed lengths need to rerun create_prob_dist
        self.seed_lengths = set()

    def _build_sentence(self, seed):
        """
        Constructs a markov chain sentence from the probability
        distribution.

        Parameters
        ----------
        seed : list
            The words that will start the sentence.
        """
        token = ''
        tokens = seed[:]  # copy seed list
        seed_length = len(seed)
        if not self.prob_dist or seed_length not in self.seed_lengths:
            self.create_prob_dist(current_state_len=len(seed))
            self.seed_lengths.add(seed_length)

        while token not in set('.?!׃\n'):
            last_tokens = tuple(tokens[-seed_length:])
            new_token = choice(self.prob_dist[last_tokens])
            tokens.append(new_token)
            token = new_token

        sentence = ' '.join(tokens)
        sentence = re.sub(r'\s+([.,?!:;׃])', r'\1', sentence)

        return sentence

    def create_prob_dist(self, current_state_len=3):
        """
        Convert a text file into a dictionary of current-state keys and
        possible next-state values. (Not *technically* a probability
        distribution.)

        {(word1, word2, word3, ...): [next1, next2, ...], ...}

        Parameters
        ----------
        current_state_len : integer, 3 by default.
            The number of tokens to be used for the current state. Must
            be >= 1.
        """
        sentences = sent_tokenize(self.text)
        state_nexts = defaultdict(list)
        for sentence in sentences:
            tokens = re.findall(self.token_pattern, sentence)
            nwise_ = nwise(tokens, n=current_state_len + 1)
            if nwise_:
                for tokens in nwise_:
                    curr_state = tuple(tokens[:-1])
                    next_state = tokens[-1]
                    state_nexts[curr_state].append(next_state)

        self.prob_dist = state_nexts

    def create_utterance(self, sent_start, char_limit=None):
        """
        Create a markov chain from a sentence start using
        a given probability distribution and returning the chain
        as a string.

        Parameters
        ----------
        sent_start : string
            A string of one or more words that occurs in the the original
            text.

        char_limit : integer, None by default.
            If None, do not use a character limit.

            Otherwise, do not return a markov string unless the total number
            of characters is <= this character limit.
        """
        too_long = True

        while too_long:
            sentence = re.findall(self.token_pattern, sent_start)

            utterance = self._build_sentence(sentence)
            len_utterance = len(utterance)

            if char_limit is not None and len_utterance > char_limit:
                too_long = True
            else:
                too_long = False

        self.utterance = utterance
        return utterance

