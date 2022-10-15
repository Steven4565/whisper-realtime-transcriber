import os
import timeit
import whisper
import numpy

from WhisperModel import Model

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

    def __test_encoder(self, audio_path: str):
        audio_byte = super().read_audio(audio_path)
        prediction = super().encode(audio_byte)       
        ground_truth = whisper.load_audio(audio_path)

        if (prediction == ground_truth).all():
            print(f"Encoder: Passed!")
        else:
            print(f"Encoder: Not Passed!\nPrediction: \n{prediction}\nGround Truth:\n{ground_truth}\n\n")

        return prediction
        
    def __test_prediction(self, audio: numpy.ndarray):
        prediction= super().predict(audio)
        print(f"Prediction: {prediction.text}\t")

if __name__ == "__main__":
    # Unit Test
    test = unit_test("small")