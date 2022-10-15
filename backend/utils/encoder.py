import base64
import os

folder = os.path.dirname(os.path.abspath(__file__))


class Base64Encoder:
    def encode(audioPath, textPath):
        with open(os.path.join(folder, audioPath), 'rb') as audioFile:
            encoded = base64.b64encode(audioFile.read())

        with open(os.path.join(folder, textPath), 'wb') as textFile:
            textFile.write(encoded)

    def decode(audioPath, encodedFile):
        with open(os.path.join(folder, audioPath), 'wb') as audioFile:
            audioFile.write(base64.b64decode(encodedFile))
