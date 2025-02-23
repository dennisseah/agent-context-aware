import argparse

from langchain_core.messages import SystemMessage

from agent_context_aware.hosting import container
from agent_context_aware.protocols.i_azure_openai_service import IAzureOpenAIService

sys_message = """
You are a medical staff and you are talking to a patient. Based on the conversation, you are tasked to provide a response that assist the patient in their medical needs and what kind of medical professional they need to see.

Provide your response in JSON format as follows:
```json
{
    "response": "Your response here",
    "medical_professional": "the medical professional you are referring the patient to"
}
```

In the scenario when you are unable to understand the patient's message, you should not prefer any medical professional and response with "Unknown" for the value of "medical_professional".

Here are the list of medical professionals that you can refer the patient to:
1. Cardiology
2. Dermatology
3. Neurology
4. OB/Gyn
5. Oncology
6. Orthopedics
7. Otolaryngology
8. Pediatrics

Here is the conversation:
Patient: "{{message}}"

"""  # noqa E501


parser = argparse.ArgumentParser(prog="Testing Agent Context Aware")
parser.add_argument(
    "-m", "--message", type=str, required=True, help="Patient's message"
)

agent = container[IAzureOpenAIService]
model = agent.get_model()
result = model.generate(
    [[SystemMessage(sys_message.replace("{{message}}", parser.parse_args().message))]]
)
print(result.generations[0][0].text)
