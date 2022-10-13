import os
import ffmpeg
import timeit
import whisper
import numpy

from WhisperModel import Model

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
        prediction = super().encode(audio_byte)       
        ground_truth = whisper.load_audio(audio_path)

        if (prediction == ground_truth).all():
            print(f"Encoder: Passed!")
        else:
            print(f"Encoder: Not Passed!\nPrediction: \n{prediction}\nGround Truth:\n{ground_truth}\n\n")

        return prediction
        
    def __test_prediction(self, audio: numpy.ndarray):
        prediction, t = super().predict(audio)
        print(f"Prediction: {prediction.text}\t{t}s")

if __name__ == "__main__":
    # Unit Test
    test = unit_test("small")