import stanza
import langid

LANGUAGE_CODE = "ug"

with open("lexicon.dic", "r", encoding="utf-8") as f:
    wordlist = [line.strip() for line in f]

# Download Uyghur model (will use UD_Uyghur-UDT under the hood)
stanza.download(LANGUAGE_CODE)
nlp = stanza.Pipeline(LANGUAGE_CODE)  # default processors: tokenize, mwt, pos, lemma, depparse

input = "سىزنىڭ ئىسمىڭىزنى بىلمەيمەن."

if langid.classify(input)[0] == LANGUAGE_CODE:
    doc = nlp(input)
    match_count = 0
    total_count = 0
    for sentence in doc.sentences:
        for word in sentence.words:
            # print(f"{word.lemma}")
            # Exclude punctuation
            if word.upos != "PUNCT":
                total_count += 1
                if word.lemma in wordlist:
                    match_count += 1
    if total_count > 0:
        print(f"{match_count}/{total_count}")
    else:
        print("No valid words to check.")
else:
    print("Input language does not match.")

