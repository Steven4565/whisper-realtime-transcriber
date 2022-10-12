import whisper
import numpy
import timeit


class Model:
    def __init__(self, model: str) -> None:
        self.model = whisper.load_model(model)
        self.options = whisper.DecodingOptions(language="en")

    def predict(self, audio: numpy.ndarray):
        # count the time elapsed for every predictions
        timer_start = timeit.default_timer()

        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        result = whisper.decode(self.model, mel, self.options)

        return result, timeit.default_timer() - timer_start

    def encode(self, audio: bytearray):
        return numpy.frombuffer(audio, numpy.int16).flatten().astype(numpy.float32) / 32768.0


whisperModelInstance = Model('tiny')
