import stanza
import langid
import torch

LANGUAGE_CODE = "ug"

with open("dictionary/lexicon.dic", "r", encoding="utf-8") as f:
    wordlist = [line.strip() for line in f]

# Download Uyghur model (will use UD_Uyghur-UDT under the hood)
stanza.download(LANGUAGE_CODE)
use_gpu = torch.cuda.is_available()
print(f"GPU enabled: {use_gpu}")
nlp = stanza.Pipeline(LANGUAGE_CODE, use_gpu=use_gpu)  # default processors: tokenize, mwt, pos, lemma, depparse

def is_uyghur_sentence(sentences, threshold=0.5):
    from langid import classify

    results = []
    uyghur_indices = [i for i, s in enumerate(sentences) if classify(s)[0] == LANGUAGE_CODE]
    uyghur_sents = [sentences[i] for i in uyghur_indices]

    if uyghur_sents:
        docs = nlp.bulk_process(uyghur_sents)
        idx = 0
        for doc in docs:
            sentence_info = {
                "sentence": uyghur_sents[idx],
                "in_wordlist": [],
                "not_in_wordlist": [],
                "word_count": 0,
                "in_wordlist_count": 0,
                "label": "no"
            }

            match_count = 0
            total_count = 0
            for sentence in doc.sentences:
                for word in sentence.words:
                    if word.upos != "PUNCT":
                        total_count += 1
                        if word.lemma in wordlist:
                            match_count += 1
                            sentence_info["in_wordlist"].append(word.lemma)
                        else:
                            sentence_info["not_in_wordlist"].append(word.lemma)

            ratio = match_count / total_count if total_count > 0 else 0
            sentence_info["word_count"] = total_count
            sentence_info["in_wordlist_count"] = match_count
            if ratio >= threshold:
                sentence_info["label"] = "ug"

            results.insert(uyghur_indices[idx], sentence_info)
            idx += 1

    # Add default output for non-Uyghur sentences
    for i, sent in enumerate(sentences):
        if not any(r.get("sentence") == sent for r in results):
            results.insert(i, {
                "sentence": sent,
                "in_wordlist": [],
                "not_in_wordlist": [],
                "word_count": 0,
                "in_wordlist_count": 0,
                "label": "no"
            })

    return results

if __name__ == "__main__":
    input_sentence = input("Enter a sentence: ")
    result = is_uyghur_sentence([input_sentence])  # Returns a list of dicts

    info = result[0]  # Get the first (and only) result
    print(f"\nSentence: {info['sentence']}")
    print(f"Detected Label: {'Uyghur' if info['label'] == 'ug' else 'NOT Uyghur'}")
    print(f"Total Words (excluding punctuation): {info['word_count']}")
    print(f"Words in Wordlist: {info['in_wordlist']}")
    print(f"Words NOT in Wordlist: {info['not_in_wordlist']}")
    print(f"Number of Words in Wordlist: {info['in_wordlist_count']}")