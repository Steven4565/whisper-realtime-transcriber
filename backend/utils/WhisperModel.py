import whisper
import numpy
from scipy.io import wavfile

class Model:
    def __init__(self, model: str) -> None:
        self.model = whisper.load_model(model)
        self.options = whisper.DecodingOptions(language="en")

    def read_audio(self, audio_path: str):
        out = whisper.load_audio(audio_path)
        return out

    def predict(self, audio: numpy.ndarray):
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        result = whisper.decode(self.model, mel, self.options)

        return result

    def encode(self, audio: bytearray):
        return numpy.frombuffer(audio, numpy.int16).flatten().astype(numpy.float32) / 32768.0

    def transcribe(self, audio_path: str):
        audio = self.read_audio(audio_path)
        encoded_audio = self.encode(audio)
        return self.predict(encoded_audio)

whisperModelInstance = Model('tiny')
print("Model Loaded!")