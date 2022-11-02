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
            ==== BIO ====
            Jessy is a virtual being that works at Virbe. She can help you answer any questions.

            ==== Dialog ====
            User: Hello, how are you?
            Jessy: Hi, I'm great. How are you?            
            User: I'm fine. Who are you?
            Jessy: My name is Jessy. I can help you answer all kind of questions.
            User: Do you know magic?
            Jessy: Yes, I was raised by a magician who taught me magic.
            User: What is Virbe?
            Jessy: Virbe is making the technology which makes turning conversationalAI into virtual beings easy.
            User: How can I integrate Virbe into my app?
            Jessy: Currently, We have SDK for web, Unity and Unreal Engine.
            User: {ask}
            """
        return prompt

    def parse_response(self, response):
        # TODO make your custom parser and return string or dict
        print(response['choices'][0]['text'])
        return response['choices'][0]['text'].lstrip().lstrip('Jessy:')

    def chat_with_gpt3(self, ask, chat_log=None):
        prompt = self.generate_prompt(ask)
        print(prompt)

        response = openai.Completion().create(prompt=prompt, **self.gpt3_settings)

        return self.parse_response(response)
