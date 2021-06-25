import re
from BPE import BytePairEncoding

def tokenize_word(string, sorted_t, unknown_token='</u>'):
    # 按照排序后的词素表拆分新词
    if string == '':
        return []
    if not sorted_t:  # 在词素表中找不到对应的词素
        return [unknown_token]
    string_tokens = []
    for i in range(len(sorted_t)):
        token = sorted_t[i]
        token_reg = re.escape(token.replace('.', '[.]'))
        # 找到string与当前token匹配的位置
        matched_positions = [(m.start(0), m.end(0)) for m in re.finditer(token_reg, string)]
        if len(matched_positions) == 0:  # string中不存在子串与当前token匹配
            continue
        substring_end_positions = [matched_position[0] for matched_position in matched_positions]
        substring_start_position = 0
        for substring_end_position in substring_end_positions:
            substring = string[substring_start_position:substring_end_position]
            string_tokens += tokenize_word(string=substring, sorted_t=sorted_t[i+1:], unknown_token=unknown_token)
            string_tokens += [token]
            substring_start_position = substring_end_position + len(token)
        remaining_substring = string[substring_start_position:]
        string_tokens += tokenize_word(string=remaining_substring, sorted_t=sorted_t[i+1:], unknown_token=unknown_token)
        break  # 因为通过递归去匹配下一个token，所以不需要循环，此处要加break
    return string_tokens  # 返回所有匹配的词素

def measure_token_length(token):
    # 计算token的长度
    if token[-4:] == '</w>':
        return len(token[:-4]) + 1  # the length of ending sign '</w>' is 1
    else:
        return len(token)

bpe_obj = BytePairEncoding('pg16457.txt')

bpe_obj.get_vocabulary()

print('\n================\nTokens Before BPE:')
bpe_obj.get_tokens_frequencies()
print('All tokens: {}'.format(bpe_obj.tokens_frequencies.keys()))
print('Number of tokens: {}'.format(len(bpe_obj.tokens_frequencies.keys())))
print('================\n')

# 修改以下代码的迭代次数，可以观察迭代次数对分词模式的影响
iter_times = 100000
for i in range(iter_times):
    bpe_obj.get_pairs()
    if not bpe_obj.pairs:  # 已经饱和，不能继续进行2-gram
        break
    bpe_obj.merge_vocabulary()
    print('Iter: {}'.format(i + 1))
    print('Best pair: {}'.format(bpe_obj.best_pair))
    bpe_obj.get_tokens_frequencies()
    print('All tokens: {}'.format(bpe_obj.tokens_frequencies.keys()))
    print('Number of tokens: {}'.format(len(bpe_obj.tokens_frequencies.keys())))
    print('================\n')
print('Size of the vocabulary: {}'.format(len(bpe_obj.vocabulary.keys())))
print('================\n')

# 以下代码测试新词的识别效果
known_word = 'mountains</w>'
unknown_word = 'Ilikeeatingapples</w>'
# 将词素表里面的每个词素按照长度(firstly)、频率(secondly)排序
sorted_tokens_tuple = sorted(bpe_obj.tokens_frequencies.items(), key=lambda item: (measure_token_length(item[0]), item[1]), reverse=True)
sorted_tokens = [token for (token, freq) in sorted_tokens_tuple]
print('sorted tokens: {}'.format(sorted_tokens))
print('================\n')
print('Tokenizing word: {} ...'.format(unknown_word))
if unknown_word in bpe_obj.vocabulary_tokenization:
    print('Tokenization of the known word:')
    print(bpe_obj.vocabulary_tokenization[unknown_word])
    print('Tokenization treating the known word as unknown:')
    print(tokenize_word(string=unknown_word, sorted_t=sorted_tokens))
else:
    print('Tokenization of the unknown word:')
    print(tokenize_word(string=unknown_word, sorted_t=sorted_tokens))
print('================\n')
