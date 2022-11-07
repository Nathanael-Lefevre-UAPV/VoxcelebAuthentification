import os
import json
from torch.utils.data import Dataset
from torch.utils.data.dataset import T_co

TAR = "1"
NON = "0"


class WavDataset(Dataset):
    def __init__(self, target):
        self.target = target
        self.datapath = f"{os.path.dirname(__file__)}"
        self.wavpath = f"{self.datapath}/wav"
        self.jsonpath = f"{self.datapath}/metadata/metadata_{self.target}.json"
        self.dataset = []

        if os.path.exists(self.jsonpath):
            self.load_dataset_from_json()
        else:
            self.gen_and_load_dataset()

    def __getitem__(self, index) -> T_co:
        return [f"{self.wavpath}/{self.dataset[index][0]}" for i in [0, 1]]

    def __len__(self):
        return len(self.dataset)

    def load_dataset_from_json(self):
        with open(self.jsonpath, 'r') as jsonFile:
            self.dataset = json.load(jsonFile)[self.target]

    def gen_and_load_dataset(self):
        with open(f"{self.datapath}/test_trials.txt", 'r') as oracleFile:
            errors = []
            lines = [line.rsplit() for line in oracleFile.readlines()]
            for (t, wav1, wav2) in lines:
                if t == self.target:
                    if os.path.exists(f"{self.wavpath}/{wav1}") and os.path.exists(f"{self.wavpath}/{wav2}"):
                        self.dataset.append([wav1, wav2])
                    else:
                        errors.append([wav1, wav2])
                        print("error", [wav1, wav2])

        os.makedirs(f"{self.datapath}/metadata", exist_ok=True)
        with open(self.jsonpath, 'w') as jsonFile:
            json.dump({self.target: self.dataset, "errors": errors}, jsonFile)


class TarWavDataset(WavDataset):
    def __init__(self):
        super().__init__(target=TAR)


class NonWavDataset(WavDataset):
    def __init__(self):
        super().__init__(target=NON)

