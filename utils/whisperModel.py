import whisper
import numpy
import timeit
import os
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

    def predict(self, audio: numpy.ndarray):
        # count the time elapsed for every predictions
        timer_start = timeit.default_timer()

        audio  = whisper.pad_or_trim(audio)
        mel    = whisper.log_mel_spectrogram(audio).to(self.model.device)
        result = whisper.decode(self.model, mel, self.options)

        return result, timeit.default_timer() - timer_start

    def encode(self, audio: bytearray):
        return numpy.frombuffer(audio, numpy.int16).flatten().astype(numpy.float32) / 32768.0

class unit_test(Model):
    RESOURCE_PATH = "../resources/"
    FORMAT = ["wav", "mp3"]

    def __init__(self, model: str) -> None:
        super().__init__(model)

        audio_path = os.listdir(self.RESOURCE_PATH)
        for audio in audio_path:
            for format in self.FORMAT:
                if audio.split('.')[1] == format:
                    encoded = self.__test_encoder(self.RESOURCE_PATH + audio)
                    self.__test_prediction(encoded)
    
    def __read_audio(self, audio_path: str, sr: int = SAMPLE_RATE):
        try:
            out, _ = (
                ffmpeg.input(audio_path, threads=0)
                .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
                .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

        return out

    def __test_encoder(self, audio_path: str):
        audio_byte = self.__read_audio(audio_path)
        timer_start = timeit.default_timer()
        prediction = super().encode(audio_byte)
        timer_end = timeit.default_timer()
        elapsed_time = round(timer_end - timer_start, 2)
        ground_truth = whisper.load_audio(audio_path)

        if (prediction == ground_truth).all():
            print(f"Encoder: Passed!\t{elapsed_time}s")
        else:
            print(f"Encoder: Not Passed!\t{elapsed_time}s\nPrediction: \n{prediction}\nGround Truth:\n{ground_truth}\n\n")

        return prediction
        
    def __test_prediction(self, audio: numpy.ndarray):
        prediction, t = super().predict(audio)
        print(f"Prediction: {prediction}\t{t}s")

if __name__ == "__main__":
    # Unit Test
    test = unit_test("small")