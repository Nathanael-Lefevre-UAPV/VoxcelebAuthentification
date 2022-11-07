### By Nathanaël Lefèvre ###

import requests
import urllib.parse


class ScoreRequester:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.URL = f"http://{self.IP}:{self.PORT}/api/spkrec"
        self.PREDICTION = "prediction"
        self.SCORE ="score"

    def __call__(self, wav1, wav2):
        data = {"utt_1": wav1, "utt_2": wav2}
        req = requests.get(self.URL, files=data)

        return req.json()


class AchilleScoreRequester(ScoreRequester):
    def __init__(self):
        IP = "achille.univ-avignon.fr"
        PORT = "5002"
        super().__init__(IP, PORT)


class LocalScoreRequester(ScoreRequester):
    def __init__(self):
        IP = "0.0.0.0"
        PORT = "3000"
        super().__init__(IP, PORT)


class HPScoreRequester(ScoreRequester):
    def __init__(self):
        IP = "10.42.0.1"
        PORT = "3000"
        super().__init__(IP, PORT)


if __name__ == "__main__":
    asr = AchilleScoreRequester()
    utt_1 = open("recoloc_sb/wavs/Abel_Ezechiel.wav", 'rb')
    utt_2 = open("recoloc_sb/wavs/Abi_yao_Vidal.wav", 'rb')

    print(asr(utt_1, utt_2))
