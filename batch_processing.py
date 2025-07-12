import sys
from main import is_uyghur_sentence
from tqdm import tqdm
import psutil
import time

def limit_cpu_usage(target_percent=50):
    p = psutil.Process()
    interval = 0.1
    while True:
        cpu = p.cpu_percent(interval=interval)
        if cpu > target_percent:
            time.sleep(interval)
        else:
            break

def process_file(input_file, output_file, threshold=0.5, batch_size=32, cpu_limit=50):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]
    results = []
    for i in tqdm(range(0, len(lines), batch_size), desc="Processing", unit="batch"):
        batch = lines[i:i+batch_size]
        for sentence in batch:
            limit_cpu_usage(cpu_limit)
            is_uyghur, ratio, match_count, total_count = is_uyghur_sentence(sentence, threshold)
            results.append('ug' if is_uyghur else 'no')
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(result + '\n')

if __name__ == "__main__":
    if len(sys.argv) < 5 or sys.argv[1] != '-i' or sys.argv[3] != '-o':
        print("Usage: python3 batch_processing.py -i <input_file.txt> -o <output_file.txt>")
        sys.exit(1)
    input_file = sys.argv[2]
    output_file = sys.argv[4]
    process_file(input_file, output_file)