import whisper

MODEL_TYPE = "tiny"


class WhisperModel:
    model = None

    def init_whisper(self):
        print('Loading model...')
        self.model = whisper.load_model(MODEL_TYPE)
        print('Done loading model')

    def transcribe_file(self, audioPath):
        text = self.model.transcribe(audioPath)
        print(text)
        return text


whisperModelInstance = WhisperModel()
