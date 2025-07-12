import sys

def update_dictionary(word_file, lexicon_file, output_file):
    with open(lexicon_file, 'r', encoding='utf-8') as f:
        lexicon = set(line.strip() for line in f if line.strip())
    with open(word_file, 'r', encoding='utf-8') as f:
        words = set(line.strip() for line in f if line.strip())
    new_words = sorted(words - lexicon)
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in new_words:
            f.write(word + '\n')
    print(f"Found {len(new_words)} new words not in lexicon. Saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 dic_update.py <word_file.txt> <lexicon.dic> [output_file.txt]")
        sys.exit(1)
    word_file = sys.argv[1]
    lexicon_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'new-words.txt'
    update_dictionary(word_file, lexicon_file, output_file)
