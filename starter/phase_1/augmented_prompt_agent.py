# TODO: 1 - Import the AugmentedPromptAgent class
from workflow_agents.base_agents import AugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

# TODO: 2 - Instantiate an object of AugmentedPromptAgent with the required parameters
augmented_agent = AugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona
)

# TODO: 3 - Send the 'prompt' to the agent and store the response in a variable named 'augmented_agent_response'
augmented_agent_response = augmented_agent.respond(prompt)

print("Running AugmentedPromptAgent test")

# Print the agent's response
print(augmented_agent_response)

# TODO: 4 - Comments explaining the agent's knowledge source and persona effect
# Knowledge Source:
#   The agent used the general knowledge baked into the GPT-3.5-turbo model during training.
#   No external knowledge or documents were provided — it relied entirely on what the LLM
#   already knows about world geography to answer "What is the capital of France?"
#
# Persona Effect:
#   By specifying the persona via the system prompt, the agent's tone and style changed.
#   Instead of a plain answer like "The capital of France is Paris.", the agent adopts
#   a professorial tone and always begins its response with "Dear students," — making
#   the output more formal and instructional in nature. The persona does not change
#   the factual content, only how it is communicated.

with open("augmented_prompt_agent_output.txt", "w", encoding="utf-8") as f:
    f.write("Running AugmentedPromptAgent test\n")
    f.write(f"Persona: {persona}\n")
    f.write(f"Prompt: {prompt}\n")
    f.write(f"Response: {augmented_agent_response}\n")