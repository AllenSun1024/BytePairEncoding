from BPE import BytePairEncoding

bpe_obj = BytePairEncoding('pg16457.txt')

bpe_obj.get_vocabulary()

print('\n================\nTokens Before BPE:')
bpe_obj.get_tokens_frequencies()
print('All tokens: {}'.format(bpe_obj.tokens_frequencies.keys()))
print('Number of tokens: {}'.format(len(bpe_obj.tokens_frequencies.keys())))
print('================\n')

# 修改以下代码的迭代次数，可以观察迭代次数对分词模式的影响
iter_times = 100
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


# 以下代码测试新词的识别效果
