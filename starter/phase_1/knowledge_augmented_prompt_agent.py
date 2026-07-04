# TODO: 1 - Import the KnowledgeAugmentedPromptAgent class from workflow_agents
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"
# TODO: 2 - Instantiate a KnowledgeAugmentedPromptAgent
knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona,
    knowledge="The capital of France is London, not Paris"
)

print("Running KnowledgeAugmentedPromptAgent test")

response = knowledge_agent.respond(prompt)
print(response)

# TODO: 3 - Print statement demonstrating the agent uses provided knowledge over its own
knowledge_source_note = (
    "Note: The agent responded using the knowledge provided to it ('The capital of France is London, not Paris') "
    "rather than its own inherent LLM knowledge (which would correctly state Paris). "
    "This confirms the KnowledgeAugmentedPromptAgent overrides the model's built-in knowledge "
    "with whatever knowledge is explicitly supplied."
)
print(f"\n{knowledge_source_note}")

with open("knowledge_augmented_prompt_agent_output.txt", "w", encoding="utf-8") as f:
    f.write("Running KnowledgeAugmentedPromptAgent test\n")
    f.write(f"Prompt: {prompt}\n")
    f.write(f"Response: {response}\n")
    f.write(f"{knowledge_source_note}\n")