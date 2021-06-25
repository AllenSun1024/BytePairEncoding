import re, collections

class BytePairEncoding:

    def __init__(self, text_path):
        self.data_source = text_path  # 待读取文本路径
        self.vocabulary = None  # 词表
        self.pairs = None  # 基于词素进行2-gram得到的词素对
        self.best_pair = None  # 出现频率最高的词素对，需要将这对词素merge
        self.tokens_frequencies = None  # 词素表
        self.vocabulary_tokenization = None  # 记录词表中每个词的merge程度

    def get_vocabulary(self):
        # 构建初始词表，形如：{'w o r d </w>': 128}
        self.vocabulary = collections.defaultdict(int)
        with open(self.data_source, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.strip().split()
                for word in words:
                    self.vocabulary[' '.join(list(word)) + ' </w>'] += 1

    def get_pairs(self):
        # 获取词素对，相邻词素结对且不超过单个word的范围
        self.pairs = collections.defaultdict(int)
        for word, freq in self.vocabulary.items():
            characters = word.split()
            for i in range(len(characters) - 1):
                self.pairs[characters[i], characters[i + 1]] += freq

    def merge_vocabulary(self):
        # merge频率最高的那个词素对，merge后更新词表
        out_vocabulary = {}
        self.best_pair = max(self.pairs, key=self.pairs.get)
        bigram = re.escape(' '.join(self.best_pair))
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        for word in self.vocabulary:
            w_out = p.sub(''.join(self.best_pair), word)
            out_vocabulary[w_out] = self.vocabulary[word]
        self.vocabulary = out_vocabulary

    def get_tokens_frequencies(self):
        # 根据更新后的词表，构建词素表
        self.tokens_frequencies = collections.defaultdict(int)
        self.vocabulary_tokenization = {}
        for word, freq in self.vocabulary.items():
            word_tokens = word.split()
            for token in word_tokens:
                self.tokens_frequencies[token] += freq
            self.vocabulary_tokenization[''.join(word_tokens)] = word_tokens






