import os
import json

import PyPDF2
import openai

def read_resume(path) -> str:
    # creating a pdf reader object
    reader = PyPDF2.PdfReader(path)
    contents = [page.extract_text() for page in reader.pages]
    return "\n".join(contents)

def call_openai(contents: str, question: str, name: str = "", normal_string = False) -> str:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_base = "https://api.endpoints.anyscale.com/v1"
    model = "meta-llama/Llama-2-7b-chat-hf"

    messages = [
      {
          "role": "system", 
          "content": contents,
      },
      {
          'role': 'user',
          'content': question,
      }
    ]
    answer = openai.ChatCompletion.create(
      model = model, 
      messages = messages,# drop the assistant message
      temperature = 0).choices[0].message.content
    system = 'You are a helpful recruiter that helps people find jobs. You are given the resume of a candidate, and your goal is to answer the following questions about the candidate.',

    if normal_string:
        return answer

    return json.dumps({'messages': [
        {
            'role': 'system',
            'content': system,
        },
        {
            'role': 'user',
            'content': f'{name}. {question}',
        },
        {
            'role': 'assistant',
            'content': answer,
        }
    ]})

contents = read_resume('cuong.pdf')
name = call_openai(contents, 'what is the person name?', normal_string=True)

questions = [
  'What is the person current company?',
  'Which professors this person has worked with?',
  'How many year of experience this person had?',
  'Which school did this person go to?',
  'What is the person title?',
  'Where is the person located?'
]

for q in questions:
  print(call_openai(contents, q, name))
