# AI Cheerish

AI Cheerish enhances your AI application's performance by injecting inspirational messages into prompts.

## Installation

Install with pip:


## Usage


from ai_cheerish import AICheerLib

class DummyAIClient:
def get_response(self, prompt):
return "Dummy response: " + prompt
ai_client = DummyAIClient()
cheer_ai = AICheerLib(ai_client)
response = cheer_ai.process_user_message("Hello!")
print(response)

