#!/usr/bin/env python3
"""stemmer - Porter stemmer and simple lemmatizer for English."""
import sys, json, re

def porter_stem(word):
    word = word.lower()
    if len(word) <= 2: return word
    # Step 1a
    if word.endswith("sses"): word = word[:-2]
    elif word.endswith("ies"): word = word[:-2]
    elif word.endswith("ss"): pass
    elif word.endswith("s"): word = word[:-1]
    # Step 1b
    if word.endswith("eed"):
        if _measure(word[:-3]) > 0: word = word[:-1]
    elif word.endswith("ed"):
        stem = word[:-2]
        if _has_vowel(stem):
            word = stem
            word = _step1b2(word)
    elif word.endswith("ing"):
        stem = word[:-3]
        if _has_vowel(stem):
            word = stem
            word = _step1b2(word)
    # Step 2
    step2 = {"ational":"ate","tional":"tion","enci":"ence","anci":"ance","izer":"ize",
             "abli":"able","alli":"al","entli":"ent","eli":"e","ousli":"ous",
             "ization":"ize","ation":"ate","ator":"ate","alism":"al","iveness":"ive",
             "fulness":"ful","ousness":"ous","aliti":"al","iviti":"ive","biliti":"ble"}
    for suffix, repl in step2.items():
        if word.endswith(suffix) and _measure(word[:-len(suffix)]) > 0:
            word = word[:-len(suffix)] + repl; break
    # Step 3
    step3 = {"icate":"ic","ative":"","alize":"al","iciti":"ic","ical":"ic","ful":"","ness":""}
    for suffix, repl in step3.items():
        if word.endswith(suffix) and _measure(word[:-len(suffix)]) > 0:
            word = word[:-len(suffix)] + repl; break
    return word

def _measure(stem):
    cv = re.sub(r'[aeiou]+', 'V', re.sub(r'[^aeiou]+', 'C', stem))
    return cv.count("VC")

def _has_vowel(stem):
    return bool(re.search(r'[aeiou]', stem))

def _step1b2(word):
    if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
        return word + "e"
    if len(word) >= 2 and word[-1] == word[-2] and word[-1] not in "lsz":
        return word[:-1]
    if _measure(word) == 1 and re.match(r'.*[^aeiou][aeiou][^aeiouwxy]$', word):
        return word + "e"
    return word

LEMMA_MAP = {"running":"run","ran":"run","better":"good","best":"good","mice":"mouse",
             "children":"child","went":"go","gone":"go","was":"be","were":"be","is":"be",
             "are":"be","been":"be","had":"have","has":"have","doing":"do","did":"do",
             "said":"say","made":"make","took":"take","came":"come","gave":"give"}

def lemmatize(word):
    return LEMMA_MAP.get(word.lower(), word.lower())

def main():
    words = ["running","jumps","easily","caresses","ponies","ties","agreed","plastered",
             "bled","motoring","sing","conflated","troubled","sized","hopping","tanned",
             "falling","hissing","fizzed","failing","filing"]
    print("Porter stemmer demo\n")
    for w in words:
        print(f"  {w:15s} -> {porter_stem(w)}")
    print(f"\nLemmatizer:")
    for w in ["running","went","better","mice","children"]:
        print(f"  {w:15s} -> {lemmatize(w)}")

if __name__ == "__main__":
    main()
