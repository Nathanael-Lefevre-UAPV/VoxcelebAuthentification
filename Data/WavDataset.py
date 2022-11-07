import os
import json
from torch.utils.data import Dataset
from torch.utils.data.dataset import T_co

TAR = "1"
NON = "0"


class WavDataset(Dataset):
    def __init__(self, target, length=0):
        self.target = target
        self.datapath = f"{os.path.dirname(__file__)}"
        self.wavpath = f"{self.datapath}/wav"
        self.jsonpath = f"{self.datapath}/metadata/metadata_{self.target}.json"
        self.dataset = []

        if os.path.exists(self.jsonpath):
            self.load_dataset_from_json()
        else:
            self.gen_and_load_dataset()
        if length == 0:
            self.len = len(self.dataset)
        else:
            self.len = len(self.dataset) if length > len(self.dataset) else length

    def __getitem__(self, index) -> T_co:
        if index >= self.len:
            raise StopIteration
        return [f"{self.wavpath}/{self.dataset[index][i]}" for i in [0, 1]]

    def __len__(self):
        return self.len

    def load_dataset_from_json(self):
        with open(self.jsonpath, 'r') as jsonFile:
            self.dataset = json.load(jsonFile)[self.target]
            print(self.dataset[0])

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
    def __init__(self, length=0):
        super().__init__(target=TAR, length=length)


class NonWavDataset(WavDataset):
    def __init__(self, length=0):
        super().__init__(target=NON, length=length)

