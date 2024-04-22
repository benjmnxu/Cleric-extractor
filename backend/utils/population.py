from utils.models import GetQuestionAndFactsResponse
from utils.agents import *

extractor = Extractor()
merger = Merger()

def populate_facts(model_instance: GetQuestionAndFactsResponse, logs: list):
    previous_message = ""
    current_message = ""
    # message = extractor.extract(model_instance.question, "\n".join(logs))
    for i, log in enumerate(logs):
        if i == 0:
            previous_message = extractor.extract(model_instance.question, log)
        else:
            current_message = extractor.extract(model_instance.question, log)
            # print(f"previous: {previous_message}")
            # print(f"current: {current_message}")
            previous_message = merger.merge(current_message, previous_message)
            # print(f"merge: {previous_message}")
    # print(message)
    # print(merger.reconcile("\n".join(message)))
    
    model_instance.status = "done"
    model_instance.facts = previous_message
    return model_instance