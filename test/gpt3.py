import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

contents = ""
while True:
    try:
        line = input()
    except EOFError:
        break
    contents += '\n' + line

# print(contents)

response = openai.Completion.create(
    model="text-davinci-002",
    prompt=contents,
    temperature=0,
    max_tokens=500,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)
print(response.choices[0].text)
