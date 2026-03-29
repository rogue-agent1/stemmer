#!/usr/bin/env python3
"""stemmer - Porter stemmer and basic text normalization."""
import sys, re

def porter_stem(word):
    word = word.lower()
    if len(word) <= 2:
        return word
    # Step 1a
    if word.endswith("sses"): word = word[:-2]
    elif word.endswith("ies"): word = word[:-2]
    elif word.endswith("ss"): pass
    elif word.endswith("s"): word = word[:-1]
    # Step 1b
    if word.endswith("eed"):
        stem = word[:-3]
        if _measure(stem) > 0:
            word = word[:-1]
    elif word.endswith("ed"):
        stem = word[:-2]
        if _has_vowel(stem):
            word = stem
            word = _step1b_fix(word)
    elif word.endswith("ing"):
        stem = word[:-3]
        if _has_vowel(stem):
            word = stem
            word = _step1b_fix(word)
    return word

def _has_vowel(stem):
    return bool(re.search(r"[aeiou]", stem))

def _measure(stem):
    return len(re.findall(r"[aeiou]+[^aeiou]+", stem))

def _step1b_fix(word):
    if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
        return word + "e"
    if len(word) >= 2 and word[-1] == word[-2] and word[-1] not in "lsz":
        return word[:-1]
    if _measure(word) == 1 and re.match(r".*[^aeiou][aeiou][^aeiouwxy]$", word):
        return word + "e"
    return word

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.split()

def tokenize_sentences(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())

STOP_WORDS = {"the","a","an","is","are","was","were","be","been","being","have","has","had",
              "do","does","did","will","would","shall","should","may","might","must","can","could",
              "i","me","my","we","our","you","your","he","him","his","she","her","it","its",
              "they","them","their","this","that","these","those","am","in","on","at","to","for",
              "of","with","by","from","as","into","through","during","before","after","and","but",
              "or","nor","not","no","so","if","then","than","too","very","just","about","above"}

def remove_stopwords(tokens):
    return [t for t in tokens if t not in STOP_WORDS]

def test():
    assert porter_stem("running") == "run"
    assert porter_stem("flies") == "fli"
    assert porter_stem("caresses") == "caress"
    assert porter_stem("cats") == "cat"
    tokens = normalize("Hello, World! This is a Test.")
    assert tokens == ["hello", "world", "this", "is", "a", "test"]
    cleaned = remove_stopwords(tokens)
    assert "hello" in cleaned and "is" not in cleaned
    sents = tokenize_sentences("Hello world. How are you? Fine.")
    assert len(sents) == 3
    print("OK: stemmer")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: stemmer.py test")
