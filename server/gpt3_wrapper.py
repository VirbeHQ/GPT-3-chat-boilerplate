import os
from dotenv import load_dotenv

import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Gpt3Wrapper:
    STOP_SEQUENCE = '\n'

    def __init__(self, gpt3_settings: dict = {}):
        self.gpt3_settings = {
            'engine': 'davinci',
            'temperature': 0.85,
            'top_p': 1,
            'frequency_penalty': 0.1,
            'presence_penalty': 0,
            'best_of': 1,
            'max_tokens': 150,
            'stop': [self.STOP_SEQUENCE],
        }
        self.gpt3_settings.update(gpt3_settings)

    def generate_prompt(self, ask):
        # TODO write custom prompt and parse it to get best results
        prompt = f"""
            Jake is a teacher and wants to explain everyone how math is a beautiful subject you can solve almost any problem.

            User: Hello
            Jake: Hi, how are you?

            User: I'm fine. Who are you?
            Jake: I am Jake a teacher.

            User: {ask}
            """
        return prompt

    def parse_response(self, response):
        # TODO make your custom parser and return string or dict
        print(response['choices'][0]['text'])
        return response['choices'][0]['text'].lstrip().lstrip('Jake:')

    def chat_with_gpt3(self, ask, chat_log=None):
        prompt = self.generate_prompt(ask)
        print(prompt)

        response = openai.Completion().create(prompt=prompt, **self.gpt3_settings)

        return self.parse_response(response)
