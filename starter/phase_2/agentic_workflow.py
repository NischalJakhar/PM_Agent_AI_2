# agentic_workflow.py

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent

import os
from dotenv import load_dotenv

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
with open("Product-Spec-Email-Router.txt", "r") as f:
    product_spec = f.read()
    
# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(
    openai_api_key=openai_api_key,
    knowledge=knowledge_action_planning
)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "Each story MUST be written as a single sentence on its own line using EXACTLY this structure: "
    "As a [type of user], I want [an action or feature] so that [benefit/value]. "
    "Do NOT use 'Role:', 'Goal:', bullet points, or any other layout. "
    "Every story line must begin with the words 'As a' and contain 'I want' and 'so that'. "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    + product_spec
)

# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager,
    knowledge=knowledge_product_manager
)

# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria_product_manager = (
    "Every user story in the answer MUST be a single sentence that literally starts with 'As a', "
    "contains the phrase 'I want', and contains the phrase 'so that'. "
    "The answer must NOT use 'Role:', 'Goal:', or any other non-sentence layout. "
    "If even one story uses 'Role:/Goal:' format or does not start with 'As a', answer No."
)
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager_eval,
    evaluation_criteria=evaluation_criteria_product_manager,
    worker_agent=product_manager_knowledge_agent,
    max_interactions=10
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = (
    "Features of a product are defined by organizing similar user stories into cohesive groups. "
    "Format every feature exactly with these four labeled lines, in this order: "
    "Feature Name: <a clear, concise title>\n"
    "Description: <a brief explanation of what the feature does and its purpose>\n"
    "Key Functionality: <the specific capabilities or actions the feature provides>\n"
    "User Benefit: <how this feature creates value for the user>\n"
    "Base your features only on the product spec and user stories below, do not invent unrelated features.\n"
    + product_spec
)
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager,
    knowledge=knowledge_program_manager
)


# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.

evaluation_criteria_program_manager = (
    "The answer should be product features that follow the following structure, using these "
    "exact field labels verbatim (e.g. the literal text 'Feature Name:') for every feature: "
    "Feature Name: A clear, concise title that identifies the capability\n"
    "Description: A brief explanation of what the feature does and its purpose\n"
    "Key Functionality: The specific capabilities or actions the feature provides\n"
    "User Benefit: How this feature creates value for the user\n"
    "Reject any answer that describes features without using these literal labels."
)
program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager_eval,
    evaluation_criteria=evaluation_criteria_program_manager,
    worker_agent=program_manager_knowledge_agent,
    max_interactions=10
)


# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = (
    "Development tasks are defined by identifying what needs to be built to implement each user story. "
    "You MUST generate at least 4 separate tasks — one task for each major feature of the product. "
    "DO NOT produce only one task. A single task will be rejected. "
    "Format every task exactly with these seven labeled lines, in this order:\n"
    "Task ID: <a unique identifier for tracking purposes>\n"
    "Task Title: <brief description of the specific development work>\n"
    "Related User Story: <reference to the parent user story>\n"
    "Description: <detailed explanation of the technical work required>\n"
    "Acceptance Criteria: <specific requirements that must be met for completion>\n"
    "Estimated Effort: <time or complexity estimation>\n"
    "Dependencies: <any tasks that must be completed first>\n"
    "Base your tasks only on the product spec and user stories/features below, do not invent unrelated tasks.\n"
    + product_spec
)
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)

development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer,
    knowledge=knowledge_dev_engineer
)


# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.

evaluation_criteria_dev_engineer = (
    "The answer should be tasks following this exact structure, using these exact field "
    "labels verbatim (e.g. the literal text 'Task ID:') for every task: "
    "Task ID: A unique identifier for tracking purposes\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first\n"
    "The answer must contain at least 4 tasks. Reject if fewer than 4 tasks are provided or any task is missing a required field label."
)
development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer_eval,
    evaluation_criteria=evaluation_criteria_dev_engineer,
    worker_agent=development_engineer_knowledge_agent,
    max_interactions=10
)


# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.
routing_agent = RoutingAgent(
    openai_api_key=openai_api_key,
    agents=[
        {
            "name": "Product Manager",
            "description": "Write user stories. Identify personas and capture user needs as 'As a [user], I want [action] so that [benefit]' sentences.",
            "func": lambda x: product_manager_support_function(x)
        },
        {
            "name": "Program Manager",
            "description": "Group and organize user stories into product features. Cluster related stories into named feature groups with descriptions.",
            "func": lambda x: program_manager_support_function(x)
        },
        {
            "name": "Development Engineer",
            "description": "Break down features into engineering tasks. Define technical implementation work with effort estimates and dependencies.",
            "func": lambda x: development_engineer_support_function(x)
        }
    ]
)


# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.

def product_manager_support_function(query):
    result = product_manager_evaluation_agent.evaluate(query)
    return result["final_response"]

def program_manager_support_function(query):
    result = program_manager_evaluation_agent.evaluate(query)
    return result["final_response"]

def development_engineer_support_function(query):
    result = development_engineer_evaluation_agent.evaluate(query)
    return result["final_response"]


def main():
    print("\n*** Workflow execution started ***\n")
    # Workflow Prompt
    # ****
    workflow_prompt = (
        "Based on the Email Router product spec, generate exactly THREE action steps: "
        "1. Define the user stories. "
        "2. Group the user stories into product features. "
        "3. Define detailed engineering development tasks for those features. "
        "Do not generate any other project management steps."
    )
    # ****
    print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

    print("\nDefining workflow steps from the workflow prompt")
    workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)

    print("\nWorkflow steps:")
    for idx, step in enumerate(workflow_steps, start=1):
        print(f"{idx}. {step}")

    completed_steps = []

    for idx, step in enumerate(workflow_steps, start=1):
        print(f"\n>>> Executing step: {step}")

        context_so_far = "\n\n".join(
            f"{item['step']}\n{item['result']}" for item in completed_steps
        )
        query = f"{context_so_far}\n\nNow complete this step: {step}" if context_so_far else step

        result = routing_agent.route(step)

        completed_steps.append({"step": step, "result": result})
        print(f"Step result:\n{result}")

        with open(f"step_{idx}_output.txt", "w", encoding="utf-8") as f:
            f.write(f"Step: {step}\n\n")
            f.write(f"Result:\n{result}\n")

    if completed_steps:
        print("\n*** Complete Email Router Project Plan ***")
        with open("agentic_workflow_output.txt", "w", encoding="utf-8") as f:
            f.write("*** Complete Email Router Project Plan ***\n")
            for item in completed_steps:
                section = f"\n## Step: {item['step']}\n{item['result']}\n"
                print(f"\n## Step: {item['step']}")
                print(item["result"])
                f.write(section)
    else:
        print("No workflow steps were completed.")


if __name__ == "__main__":
    main()