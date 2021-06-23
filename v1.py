import re, collections

class BytePairEncoding:
    def __init__(self, data_path):
        # assign the data source
        self.data_path = data_path
        self.vocab = None  # vocabulary dict, {"string": int}
        self.pairs = None  # pairs dict, {('char', 'char'): int}
        self.tokens = None
        self.token_len_history = []

    def get_vocab(self):
        # build the vocabulary
        vocab = collections.defaultdict(int)
        with open(self.data_path, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.strip().split()
                # split each word into characters, represent each word as a sequence of characters
                for word in words:
                    vocab[' '.join(list(word)) + ' </w>'] += 1
        self.vocab = vocab

    def get_pairs(self):
        # pair two adjacent characters, do not consider pairs that cross word boundaries
        pairs = collections.defaultdict(int)
        for word, freq in self.vocab.items():
            characters = word.split()
            for i in range(len(characters) - 1):
                pairs[characters[i], characters[i + 1]] += freq
        self.pairs = pairs

    def merge_vocab(self):
        # merge the best pair and update the vocabulary
        v_out = {}
        best_pair = max(self.pairs, key=self.pairs.get)
        bigram = re.escape(' '.join(best_pair))
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        for word in self.vocab:
            w_new = p.sub(''.join(best_pair), word)
            v_out[w_new] = self.vocab[word]
        self.vocab = v_out

    def get_tokens(self):
        # before merge -> vocabulary item: 'c a b c d </w>'  token: 'a', 'b', 'c'(2), 'd', '</w>'
        # after merge -> vocabulary item: 'c a b cd </w>'  token: 'a', 'b', 'c'(1), 'cd', '</w>'
        # get the tokens according to the vocabulary after merged
        self.tokens = collections.defaultdict(int)
        for word, freq in self.vocab.items():
            word_tokens = word.split()
            for token in word_tokens:
                self.tokens[token] += freq
        self.token_len_history.append(len(self.tokens))


bpe = BytePairEncoding("pg16457.txt")
bpe.get_vocab()
iter_times = 100000
for i in range(iter_times):
    bpe.get_pairs()
    if not bpe.pairs:
        break
    bpe.merge_vocab()
    bpe.get_tokens()
print(bpe.token_len_history[len(bpe.token_len_history) - 1])
