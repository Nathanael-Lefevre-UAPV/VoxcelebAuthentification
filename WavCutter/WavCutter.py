import torch
import torchaudio
import matplotlib.pyplot as plt


class WavTimer:
    units = {"s": 1,
             "ms": 0.001}
    unit_name = {"s": "seconde",
                 "ms": "milli-seconde"}

    @staticmethod
    def get_duration(waveform, samplerate, unit="ms"):
        return (waveform.shape[1] / WavTimer.units[unit]) / samplerate

    @staticmethod
    def convert_to_n_frame(duration, samplerate, unit="ms"):
        return duration * WavTimer.units[unit] * samplerate


class WavCutter:
    def cut(self, waveform, samplerate, start, duration=None, end=None, unit="ms"):
        assert not(duration is None and end is None)
        assert None in [duration, end]

        start_frame = int(WavTimer.convert_to_n_frame(start, samplerate, unit=unit))

        assert 0 <= start_frame < waveform.shape[1]

        if end is not None:
            end_frame = int(WavTimer.convert_to_n_frame(end, samplerate, unit=unit))
        else:
            end_frame = int(WavTimer.convert_to_n_frame(start + duration, samplerate, unit=unit))

        assert 0 < end_frame <= waveform.shape[1]
        assert start_frame < end_frame

        print("start_frame", start_frame)
        print("end_frame", end_frame)

        print("waveform", waveform)
        new_waveform = torch.cat((waveform[0][0:start_frame],
                                  waveform[0][end_frame:]),
                                 dim=0).unsqueeze(0)

        print("new_waveform", new_waveform)

        return new_waveform, samplerate







if __name__ == "__main__":
    filename = "../recoloc_sb/wavs/Abel_Ezechiel.wav"

    with open(filename, 'rb') as wav:
        waveform, samplerate = torchaudio.load(wav)
        print("time", WavTimer.get_duration(waveform, samplerate))

        plt.figure()
        plt.plot(waveform.t().numpy())
        plt.show()
        plt.close()

        wc = WavCutter()
        waveform, samplerate = wc.cut(waveform, samplerate, start=0, end=1000, unit="ms")

        print("time", WavTimer.get_duration(waveform, samplerate))

        plt.figure()
        plt.plot(waveform.t().numpy())
        plt.show()
        plt.close()

