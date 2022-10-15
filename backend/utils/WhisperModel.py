import whisper
import numpy
import timeit
import ffmpeg

def exact_div(x, y):
    assert x % y == 0
    return x // y

SAMPLE_RATE = 16000
N_FFT = 400
N_MELS = 80
HOP_LENGTH = 160
CHUNK_LENGTH = 30
N_SAMPLES = CHUNK_LENGTH * SAMPLE_RATE  # 480000: number of samples in a chunk
N_FRAMES = exact_div(N_SAMPLES, HOP_LENGTH)  # 3000: number of frames in a mel spectrogram input

class Model:
    def __init__(self, model: str) -> None:
        self.model = whisper.load_model(model)
        self.options = whisper.DecodingOptions(language="en")

    def read_audio(self, audio_path: str, sr: int = SAMPLE_RATE):
        try:
            out, _ = (
                ffmpeg.input(audio_path, threads=0)
                .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
                .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

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

whisperModelInstance = Model('small')
