import sys
from main import is_uyghur_sentence
from tqdm import tqdm

def main():
    # Parse arguments: -i <file> <-t|-f>
    if len(sys.argv) < 4 or sys.argv[1] != '-i' or sys.argv[3] not in ['-t', '-f']:
        print("Usage: python3 test_detection.py -i <test_file.txt> <-t|-f>")
        sys.exit(1)
    test_file = sys.argv[2]
    is_uyghur_mode = sys.argv[3] == '-t'
    with open(test_file, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]
    uyghur_detected = 0
    non_uyghur_detected = 0
    total = len(sentences)
    threshold = 0.5  # You can adjust this threshold as needed
    for sentence in tqdm(sentences, desc="Processing", unit="sent"):
        is_uyghur, ratio, match_count, total_count = is_uyghur_sentence(sentence, threshold)
        if is_uyghur:
            uyghur_detected += 1
        else:
            non_uyghur_detected += 1
    if is_uyghur_mode:
        accuracy = (uyghur_detected / total) * 100 if total > 0 else 0
        print(f"Uyghur detection: {uyghur_detected}/{total} ({accuracy:.2f}%)")
        if accuracy < 90:
            print("Warning: Uyghur detection accuracy is below 90%")
    else:
        accuracy = (non_uyghur_detected / total) * 100 if total > 0 else 0
        print(f"Non-Uyghur detection: {non_uyghur_detected}/{total} ({accuracy:.2f}%)")
        if accuracy < 90:
            print("Warning: Non-Uyghur detection accuracy is below 90%")

if __name__ == "__main__":
    main()
