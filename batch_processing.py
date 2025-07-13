import sys
import json
from main import is_uyghur_sentence
from tqdm import tqdm

def process_file(input_file, output_file, batch_size=512, dbmode=False):
    from tqdm import tqdm

    with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
        batch = []
        for line in tqdm(fin, desc="Reading", unit=" lines"):
            batch.append(line.strip())
            if len(batch) == batch_size:
                results = is_uyghur_sentence(batch)
                if dbmode == True:
                    fout.write('\n'.join(json.dumps(res, ensure_ascii=False) for res in results) + '\n')
                else:
                    labels = [item['label'] for item in results]
                    fout.write('\n'.join(labels) + '\n')
                batch = []
        if batch:
            results = is_uyghur_sentence(batch)
            if dbmode == True:
                fout.write('\n'.join(json.dumps(res, ensure_ascii=False) for res in results) + '\n')
            else:
                labels = [item['label'] for item in results]
                fout.write('\n'.join(labels) + '\n')

if __name__ == "__main__":
    if len(sys.argv) < 5 or sys.argv[1] != '-i' or sys.argv[3] != '-o':
        print("Usage: python3 batch_processing.py -i <input_file.txt> -o <output_file.txt> -d")
        sys.exit(1)
    input_file = sys.argv[2]
    output_file = sys.argv[4]
    debug_enable = '-d' in sys.argv
    process_file(input_file, output_file, dbmode=debug_enable)