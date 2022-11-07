import requests
from tqdm import tqdm
import io
from pathlib import Path
import torchaudio

IP = "localhost"
PORT = "3000"
URL = f"http://{IP}:{PORT}/api/spkrec"

def convert_path(path):
    return Path("wav/") / path


def get_match_lists():
    matches = []
    non_matches = []

    with open("test_trials.txt", "r+") as f:
        for line in f.read().split("\n"):
            is_match, a_path, b_path = line.split(" ")
            is_match = int(is_match) == 1

            target_list = matches if is_match else non_matches
            target_list.append((convert_path(a_path), convert_path(b_path)))

    return matches, non_matches


def evaluate_similarity(a_waveform, b_waveform, sample_rate):
    a_file = audio_tensor_to_filelike(a_waveform, sample_rate)
    b_file = audio_tensor_to_filelike(b_waveform, sample_rate)

    request_files = {"utt_1": a_file, "utt_2": b_file}
    request = requests.get(URL, files=request_files)
    return request.json()


def audio_tensor_to_filelike(waveform, sample_rate):
    output_file = io.BytesIO()
    torchaudio.save(output_file, waveform, sample_rate, format="wav")
    output_file.seek(0)
    return output_file


matches, non_matches = get_match_lists()

a_path, b_path = non_matches[2]
a, a_sr = torchaudio.load(a_path)
b, b_sr = torchaudio.load(b_path)
assert a_sr == b_sr
print(evaluate_similarity(a, b, a_sr))