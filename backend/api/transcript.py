from utils.WhisperModel import whisperModelInstance
from flask import request
from flask_restful import Resource
from utils.encoder import Base64Encoder
import os
import base64

RECORDING_PATH = os.path.join(
    os.getcwd(), 'resources', 'recording.mp3')

class Transcript(Resource):
    def post(self):
        # get data from request
        data = request.data.decode("utf-8")

        # decode data into byte-array
        # Base64Encoder.decode(RECORDING_PATH, data.split('base64,')[1])
        # whisperModelInstance.read_audio(RECORDING_PATH)
        # transcribe the audio
        # transcript = whisperModelInstance.transcribe(RECORDING_PATH).text

        # return transcript