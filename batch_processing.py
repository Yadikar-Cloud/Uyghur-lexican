import stanza
import langid
import tqdm

LANGUAGE_CODE = "ug"

with open("lexicon.dic", "r", encoding="utf-8") as f:
    wordlist = set(line.strip() for line in f)  # Use set for faster lookup

# Enable GPU
stanza.download(LANGUAGE_CODE)
nlp = stanza.Pipeline(LANGUAGE_CODE, use_gpu=True)

def process_batch(sentences):
    results = []
    for sent in sentences:
        doc = nlp(sent)
        match_count = 0
        total_count = 0
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.upos != "PUNCT":
                    total_count += 1
                    if word.lemma in wordlist:
                        match_count += 1
        results.append((match_count, total_count))
    return results

def process_file(filename, batch_size=32):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    batch = [s for s in lines if langid.classify(s)[0] == LANGUAGE_CODE]
    results = []
    for i in tqdm.tqdm(range(0, len(batch), batch_size), desc="Processing", unit="batch"):
        batch_slice = batch[i:i+batch_size]
        results.extend(process_batch(batch_slice))
    return results

# Example: batch of sentences
inputs = ["سىزنىڭ ئىسمىڭىزنى بىلمەيمەن.", "مېنىڭ دوستۇم بەك ياخشى"]
batch = [s for s in inputs if langid.classify(s)[0] == LANGUAGE_CODE]
results = process_batch(batch)
for match_count, total_count in results:
    print(f"{match_count}/{total_count}")

if __name__ == "__main__":
    results = process_file("newfile.txt")
    for match_count, total_count in results:
        print(f"{match_count}/{total_count}")