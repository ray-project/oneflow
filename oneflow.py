import PyPDF2
import json
import openai
import os
import time

SYSTEM_MESSAGE = (
    "You are a helpful recruiter that helps people find jobs. You are "
    "given the resume of a candidate, and your goal is to answer the "
    "following questions about the candidate."
)


def read_resume(path) -> str:
    # creating a pdf reader object
    reader = PyPDF2.PdfReader(path)
    _contents = [page.extract_text() for page in reader.pages]
    return "\n".join(_contents)


def call_openai(
    _contents: str,
    question: str,
    _name: str = "",
    normal_string=False
) -> str:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_base = "https://api.endpoints.anyscale.com/v1"
    model = "meta-llama/Llama-2-7b-chat-hf"

    messages = [
      {
          "role": "system",
          "content": _contents,
      },
      {
          'role': 'user',
          'content': question,
      }
    ]
    answer = openai.ChatCompletion.create(
      model=model,
      messages=messages,
      temperature=0
    ).choices[0].message.content

    if normal_string:
        return answer

    return json.dumps({'messages': [
        {
            'role': 'system',
            'content': SYSTEM_MESSAGE,
        },
        {
            'role': 'user',
            'content': question,
        },
        {
            'role': 'assistant',
            'content': f"{_name}. {answer}",
        }
    ]})


def extract_data(file_path: str, file_writer):
    if not file_path.endswith(".pdf"):
        return

    contents = read_resume(file_path)
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
        data = call_openai(contents, q, name).replace("\\n", ""). replace("..", ".")
        print(data)
        file_writer.write(data)
        file_writer.write("\n")


def main():
    dir_list = sorted(os.listdir('pdf'))
    with open("fined_tune.txt", "w") as f:
        for file_name in dir_list:
            start_time = time.time()
            extract_data(f"pdf/{file_name}", f)
            print(f"{file_name} took: {time.time() - start_time}s")


if __name__ == '__main__':
    main()
