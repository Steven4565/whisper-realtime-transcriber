from utils.WhisperModel import whisperModelInstance
from flask import request
from flask_restful import Resource
from utils.encoder import Base64Encoder
import soundfile as sf
import io
import os
import base64

RECORDING_PATH = os.path.join(
    os.getcwd(), 'resources', 'recording.wav')

class Transcript(Resource):
    def post(self):
        # get data from request
        data = request.data.decode('utf-8')
        Base64Encoder.decode(RECORDING_PATH, data)
        # transcript = whisperModelInstance.transcribe(RECORDING_PATH).text
        # print(transcript)
        
        # return transcript