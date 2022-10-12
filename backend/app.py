from flask import Flask
from flask_restful import Api
from api import transcript, grammar
from dotenv import load_dotenv
import os

dotenv_path = load_dotenv(os.path.join(os.getcwd(), '.env'))
load_dotenv(dotenv_path)

app = Flask('whisperapi')
api = Api(app)

api.add_resource(transcript.Transcript, '/transcript')
api.add_resource(grammar.GrammarCorrector, '/grammar')

if __name__ == '__main__':
    app.run(debug=True)
