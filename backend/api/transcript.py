from utils.WhisperModel import whisperModelInstance
from flask import request
from flask_restful import Resource
from utils.encoder import Base64Encoder
import simpleaudio as sa
import os

RECORDING_PATH = os.path.join(
    os.getcwd(), 'resources', 'recording.wav')

class Transcript(Resource):
    def post(self):
        # get data from request
        data = request.data.decode('utf-8')
        print(data)
        # # decode data into byte-array
        Base64Encoder.decode(RECORDING_PATH, data)
        # whisperModelInstance.read_audio(RECORDING_PATH)
        # # transcribe the audio
        # transcript = whisperModelInstance.transcribe(RECORDING_PATH).text

        # return transcript