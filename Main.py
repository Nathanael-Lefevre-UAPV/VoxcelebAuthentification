import operator
import tqdm

from ScoreRequester import HPScoreRequester, AchilleScoreRequester
from Data.WavDataset import TarWavDataset, NonWavDataset


class Predictor:
    def __init__(self, score_requester):
        self.scoreRequester = score_requester

    def __call__(self, wav1, wav2):
        return self.predict(wav1, wav2)

    def predict(self, wav1, wav2) -> bool:
        pass


class DefaultPredictor(Predictor):
    def predict(self, wav1, wav2):
        return self.scoreRequester(wav1, wav2)[self.scoreRequester.PREDICTION]


class ThresholdPredictor(Predictor):
    def __init__(self, score_requester, threshold, op=operator.ge):
        self.op = op
        self.threshold = threshold
        super().__init__(score_requester)

    def predict(self, wav1, wav2):
        return self.op(self.scoreRequester(wav1, wav2)[self.scoreRequester.SCORE], self.threshold)


if __name__ == "__main__":
    scoreReq = AchilleScoreRequester()

    tarWavDataset = TarWavDataset(length=10)
    nonWavDataset = NonWavDataset(length=10)
    print(len(tarWavDataset))
    print(len(nonWavDataset))

    predictor = DefaultPredictor(scoreReq)

    print(nonWavDataset[0])
    print(tarWavDataset[0])

    wavCouple = ["Data/wav/id10270/x6uYqmx31kE/00001.wav", "Data/wav/id10300/ize_eiCFEg0/00003.wav"]
    utt_1 = open(wavCouple[0], 'rb')
    utt_2 = open(wavCouple[1], 'rb')
    pred = predictor(utt_1, utt_2)
    input(pred)


    def count_negative_positive(dataset):
        count = [0, 0]  # [nbNegative, nbPositive]
        log = dict()
        i = 0
        tbar = tqdm.tqdm(dataset)
        for wavCouple in tbar:
            utt_1 = open(wavCouple[0], 'rb')
            utt_2 = open(wavCouple[1], 'rb')
            pred = predictor(utt_1, utt_2)
            tbar.set_description(str(pred) + str(wavCouple))
            #print("pred for real true:", pred)
            count[pred] += 1
            log[i] = pred
            i += 1
            input()
        print(log)
        return count

    #FN, TP = count_negative_positive(tarWavDataset)  # False Negative, True Positive
    TN, FP = count_negative_positive(nonWavDataset)  # True Negative, False Positive

    FR = FN / (TP + FN)  # False Reject
    FA = FP / (FP + TN)  # False Acceptance
    HTER = (FR + FA) / 2  # Half Total Error Rate

    result = {"FN": FN,
              "TP": TP,
              "TN": TN,
              "FP": FP,
              "FR": FR,
              "FA": FA,
              "HTER": HTER}
    print(result)
