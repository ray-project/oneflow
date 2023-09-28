import os

import PyPDF2
import openai


# creating a pdf reader object
reader = PyPDF2.PdfReader('cuong.pdf')
contents = [page.extract_text() for page in reader.pages]

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_base = "https://api.endpoints.anyscale.com/v1"
model = "meta-llama/Llama-2-7b-chat-hf"

messages = [
    {
        "role": "system", 
        "content": "\n".join(contents),
    },
    {
        'role': 'user',
        'content': 'how long have Cuong been working at Meta?',
    }
]
print(openai.ChatCompletion.create(
    model = model, 
    messages = messages,# drop the assistant message
    temperature = 0).choices[0].message.content)