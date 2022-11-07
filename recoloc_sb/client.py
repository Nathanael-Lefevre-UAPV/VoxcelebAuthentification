import requests
import urllib.parse

import time

time_start = time.time()

IP = "0.0.0.0"
PORT = "3000"
URL = f"http://{IP}:{PORT}/api/spkrec"

# Speaker is not the same
utt_1 = open("wavs/Abel_Ezechiel.wav", 'rb')
utt_2 = open("wavs/Abi_yao_Vidal.wav", 'rb')
data = {"utt_1": utt_1, "utt_2": utt_2}

req = requests.get(URL, files=data)
print(req.json())

# Speaker is the same
utt_1 = open("wavs/Abel_Ezechiel.wav", 'rb')
utt_2 = open("wavs/Abel_Ezechiel.wav", 'rb')
data = {"utt_1": utt_1, "utt_2": utt_2}

req = requests.get(URL, files=data)
print(req.json())


time_end = time.time()
time_elapsed = time_end - time_start

print(f'Temps d\'exécution : {time_elapsed:.4}s')
