import stanza
import langid
import torch

LANGUAGE_CODE = "ug"

with open("lexicon.dic", "r", encoding="utf-8") as f:
    wordlist = [line.strip() for line in f]

# Download Uyghur model (will use UD_Uyghur-UDT under the hood)
stanza.download(LANGUAGE_CODE)
use_gpu = torch.cuda.is_available()
nlp = stanza.Pipeline(LANGUAGE_CODE, use_gpu=use_gpu)  # default processors: tokenize, mwt, pos, lemma, depparse

def is_uyghur_sentence(input_sentence, threshold=0.5):
    if langid.classify(input_sentence)[0] == LANGUAGE_CODE:
        doc = nlp(input_sentence)
        match_count = 0
        total_count = 0
        for sentence in doc.sentences:
            for word in sentence.words:
                # Exclude punctuation
                if word.upos != "PUNCT":
                    total_count += 1
                    if word.lemma in wordlist:
                        match_count += 1
        if total_count > 0:
            ratio = match_count / total_count
            return ratio >= threshold, ratio, match_count, total_count
        else:
            return False, 0.0, 0, 0
    else:
        return False, 0.0, 0, 0

if __name__ == "__main__":
    input_sentence = input("Enter a sentence: ")
    is_uyghur, ratio, match_count, total_count = is_uyghur_sentence(input_sentence)
    if total_count > 0:
        print(f"{match_count}/{total_count}")
        print(f"Uyghur detected: {is_uyghur} (ratio: {ratio:.2f})")
    else:
        print("No valid words to check.")

