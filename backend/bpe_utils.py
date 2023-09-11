import logging
import re
from config import MONGO_DB

def train_bpe(corpus, vocab_size):
    logging.info("Training BPE...")
    vocab = {}
    for word in corpus.split():
        word = ' '.join(list(word)) + ' </w>'
        if word in vocab:
            vocab[word] += 1
        else:
            vocab[word] = 1
    
    for i in range(vocab_size):
        pairs = get_stats(vocab)
        if not pairs:
            break
        best_pair = max(pairs, key=pairs.get)
        vocab = merge_vocab(best_pair, vocab)
    
    return {k: v for k, v in vocab.items() if len(k.split()) == 1}

def get_stats(vocab):
    logging.info("Getting stats...")
    pairs = {}
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pair = (symbols[i], symbols[i+1])
            if pair in pairs:
                pairs[pair] += freq
            else:
                pairs[pair] = freq
    return pairs

def merge_vocab(pair, vocab):
    logging.info(f"Merging vocabulary for pair: {pair}")
    new_vocab = {}
    replacement = f"{pair[0]}{pair[1]}"
    pattern = re.compile(r'(?<!\S)' + re.escape(f"{pair[0]} {pair[1]}") + r'(?!\S)')
    for word in vocab:
        new_word = re.sub(pattern, replacement, word)
        new_vocab[new_word] = vocab[word]
    return new_vocab

def extract_last_subword(input_text, length=3):
    last_subword = input_text[-length:]
    logging.info(f"Extracted last subword: {last_subword}")
    return last_subword

def bpe_autocomplete(input_text, bpe_model):
    last_subword = extract_last_subword(input_text)
    suggestions = [word for word in bpe_model.keys() if last_subword in word]
    return suggestions
