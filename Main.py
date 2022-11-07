import operator

from ScoreRequester import HPScoreRequester
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
    scoreReq = HPScoreRequester()

    tarWavDataset = TarWavDataset()
    nonWavDataset = NonWavDataset()
    print(len(tarWavDataset))
    print(len(nonWavDataset))

    predictor = DefaultPredictor(scoreReq)

    FP = 0  # False Positive
    TN = 0  # True Negative


    def count_negative_positive(dataset):
        count = [0, 0]  # [nbNegative, nbPositive]

        for wavCouple in dataset:
            utt_1 = open(wavCouple[0], 'rb')
            utt_2 = open(wavCouple[1], 'rb')
            pred = predictor(utt_1, utt_2)
            print("pred for real true:", pred)
            count[pred] += 1

        return count

    FN, TP = count_negative_positive(tarWavDataset)  # False Negative, True Positive
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
