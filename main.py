import stanza
import langid
import torch

LANGUAGE_CODE = "ug"

with open("lexicon.dic", "r", encoding="utf-8") as f:
    wordlist = [line.strip() for line in f]

# Download Uyghur model (will use UD_Uyghur-UDT under the hood)
stanza.download(LANGUAGE_CODE)
use_gpu = torch.cuda.is_available()
print(f"GPU enabled: {use_gpu}")
nlp = stanza.Pipeline(LANGUAGE_CODE, use_gpu=use_gpu)  # default processors: tokenize, mwt, pos, lemma, depparse


def is_uyghur_sentence(sentences, threshold=0.5):
    from langid import classify
    uyghur_indices = [i for i, s in enumerate(sentences) if classify(s)[0] == LANGUAGE_CODE]
    documents = [sentences[i] for i in uyghur_indices]
    results = ['no'] * len(sentences)
    if documents:
        in_docs = [stanza.Document([], text=d) for d in documents]
        docs = nlp(in_docs)
        idx = 0
        for doc in docs:
            match_count = 0
            total_count = 0
            for sentence in doc.sentences:
                for word in sentence.words:
                    if word.upos != "PUNCT":
                        total_count += 1
                        if word.lemma in wordlist:
                            match_count += 1
            ratio = match_count / total_count if total_count > 0 else 0
            if ratio >= threshold:
                results[uyghur_indices[idx]] = 'ug'
            idx += 1
    return results

if __name__ == "__main__":    Basic
    input_sentence = input("Enter a sentence: ")
    result = is_uyghur_sentence([input_sentence])  # Pass as a list
    if result[0] == 'ug':
        print("The sentence is in Uyghur.")
    else:
        print("The sentence is NOT in Uyghur.")

