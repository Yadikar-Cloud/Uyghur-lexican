import unittest
import json
from main import is_uyghur_sentence

class TestMainUyghurDetection(unittest.TestCase):
    def setUp(self):
        with open("test_samples.json", "r", encoding="utf-8") as f:
            self.samples = json.load(f)

    def test_uyghur_detection(self):
        uyghur_correct = 0
        non_uyghur_correct = 0
        uyghur_total = 0
        non_uyghur_total = 0
        threshold = 0.5  # You can adjust this threshold as needed
        for sample in self.samples:
            sentence = sample["sentence"]
            label = sample["label"]
            is_uyghur, ratio, match_count, total_count = is_uyghur_sentence(sentence, threshold)
            if label == "ug":
                uyghur_total += 1
                if is_uyghur:
                    uyghur_correct += 1
            else:
                non_uyghur_total += 1
                if not is_uyghur:
                    non_uyghur_correct += 1
        total = uyghur_total + non_uyghur_total
        correct = uyghur_correct + non_uyghur_correct
        accuracy = (correct / total) * 100 if total > 0 else 0
        print(f"Uyghur correct: {uyghur_correct}/{uyghur_total}")
        print(f"Non-Uyghur correct: {non_uyghur_correct}/{non_uyghur_total}")
        print(f"Detection accuracy: {accuracy:.2f}%")
        self.assertGreaterEqual(accuracy, 90, "Detection accuracy is below 90%")
        self.assertEqual(uyghur_correct, uyghur_total, "Not all Uyghur sentences detected correctly")
        self.assertEqual(non_uyghur_correct, non_uyghur_total, "Not all non-Uyghur sentences detected correctly")

if __name__ == "__main__":
    unittest.main()
