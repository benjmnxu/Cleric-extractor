import openai
import os
from dotenv import load_dotenv
from utils.prompts import *

load_dotenv()

class Agent:

    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")

class Extractor(Agent):

    def extract(self, question: str, log: str):

        messages = [
            {"role": "system", "content": system_prompt_first()},
            {"role": "user", "content": question_prompt_first(question, log)}  
        ]

        extraction = openai.chat.completions.create(
            model="gpt-4",
            temperature=0.1,
            messages = messages
        )

        facts = extraction.choices[0].message.content.split("$$")

        return facts
    
class Merger(Agent):

    def reconcile(self, A: str):
        # print(user_prompt_merge(A, B))
        messages = [
            {"role": "system", "content": "You will be given a list of facts. Combine any coexisting facts into one sentence and remove any facts which contradict."},
            {"role": "user", "content": A}  
        ]
        merged_facts = openai.chat.completions.create(
            model="gpt-4",
            temperature=0.1,
            messages = messages
        )

        content = merged_facts.choices[0].message.content
        content = content.replace("&&", "")

        facts = content.split("$$")
        return facts

    def merge(self, A: list, B: list):
        # print(user_prompt_merge(A, B))
        messages = [
            {"role": "system", "content": system_prompt_merge()},
            {"role": "user", "content": user_prompt_merge(A, B)}  
        ]
        merged_facts = openai.chat.completions.create(
            model="gpt-4",
            temperature=0.1,
            messages = messages
        )

        content = merged_facts.choices[0].message.content
        content = content.replace("&&", "")

        facts = content.split("$$")
        return facts
