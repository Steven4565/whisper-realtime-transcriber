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


# Test encode
# Base64Encoder.encode("../resources/recording.mp3",
#                      "../resources/recording.txt")

# Test decode
# with open(os.path.join(folder, "../resources/recording.txt"), 'rb') as textFile:
#     Base64Encoder.decode("../resources/recordingDecoded.mp3", textFile.read())
