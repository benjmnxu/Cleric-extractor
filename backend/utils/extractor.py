import openai
import os
from dotenv import load_dotenv
from models import GetQuestionAndFactsResponse

load_dotenv()

class Extractor:

    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def extract_and_set(self, messages: list, model: GetQuestionAndFactsResponse):
        extraction = openai.chat.completions.create(
            model="gpt-4",
            temperature=0.1,
            messages = messages
        )

        print(extraction.choices[0].message.content)

        facts = extraction.choices[0].message.content.split("$$")

        model.facts = facts
        model.status = "done"