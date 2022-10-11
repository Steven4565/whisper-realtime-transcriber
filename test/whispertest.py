import whisper

model = whisper.load_model("tiny")
text = model.transcribe(
    "C:/Users/Steven/Documents/1-Computer/Competitions/OpenAIWhisperHackathon/flaskApi/resources/recording.mp3")
# printing the transcribe
print(text['text'])
