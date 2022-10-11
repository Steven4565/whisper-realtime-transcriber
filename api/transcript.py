from utils.whisperModel import whisperModelInstance
from flask import request
from flask_restful import Resource
from utils.encoder import Base64Encoder
import os


class Transcript(Resource):
    def post(self):
        data = request.data.decode("utf-8")
        RECORDING_PATH = os.path.join(
            os.getcwd(), 'resources', 'recording.mp3')
        Base64Encoder.decode(RECORDING_PATH, data)

        transcript = whisperModelInstance.transcribe_file(RECORDING_PATH)
        print(transcript["text"])
        return transcript["text"]
