from utils.models import GetQuestionAndFactsResponse
from utils.agents import *

extractor = Extractor()
merger = Merger()

def populate_facts(model_instance: GetQuestionAndFactsResponse, logs: list):
    previous_message = ""
    current_message = ""

    for i, log in enumerate(logs):
        if i == 0:
            previous_message = extractor.extract(model_instance.question, log)
        else:
            current_message = extractor.extract(model_instance.question, log)
            previous_message = merger.merge(current_message, previous_message)
    
    model_instance.status = "done"
    model_instance.facts = previous_message
    return model_instance