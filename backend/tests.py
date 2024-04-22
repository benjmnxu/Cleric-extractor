import openai
import os
from dotenv import load_dotenv
import asyncio

from utils.prompts import *
from backend.utils.population import populate_facts
from backend.utils.models import *

load_dotenv()

async def tester(i: int):
    messages = [
        {"role": "user", "content": test_generation_prompt()}  
    ]
    
    test_case = openai.chat.completions.create(
        model="gpt-4-turbo",
        temperature=0.75,
        messages = messages
    )
    test = test_case.choices[0].message.content.split("~")
    
    result = GetQuestionAndFactsResponse(question="What are our product decisions", facts=[], status="processing")
    
    populate_facts(result, test)

    with open(f"test_logs/test{i}.txt", "w") as file:
        file.write("\n".join(test))
        file.write(result.question)
        file.write("\n".join(result.facts))
    


async def main():
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    for i in range(0, 5):
        await tester(i)

asyncio.run(main())