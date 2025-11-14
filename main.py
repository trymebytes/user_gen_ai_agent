from typing import List
import json
import os
import random
import string
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

@tool
def write_json(filepath: str, data: dict) -> str:
    """Write a python dictionary to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return f"Successfully wrote JSON data to '{filepath}' ({len(json.dumps(data))} characters)."
    except Exception as e:
        return f"Error writing JSON to : {str(e)}"

@tool
def read_json(filepath: str) -> str:
    """Read a JSON file and return its contents as a formatted string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        return f"File '{filepath}' not found."
    except json.JSONDecodeError as e:
        return f"Invalid JSON in file - {str(e)}"
    except Exception as e:
        return f"Error reading JSON from file: {str(e)}"
    
@tool
def generate_user_data() -> dict:
    """Generate a list of user data dictionaries."""
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
    domains = ["example.com", "mail.com", "test.org"]

    def random_date(start, end):
        return start + timedelta(
            seconds=random.randint(0, int((end - start).total_seconds())),
        )

    users = []
    for _ in range(5):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        signup_date = random_date(
            datetime.now() - timedelta(days=365),
            datetime.now(),
        ).strftime("%Y-%m-%d")
        users.append({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "signup_date": signup_date,
        })
    return {"users": users}

TOOLS = [write_json, read_json, generate_user_data]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
SYSTEM_MSG = (
    "You are DataGen, a helpful assistant that generates sample data for applications. "
    "To generate users, you can use the 'generate_user_data' tool. "
    "To save data to a file, use the 'write_json' tool. "
    "To read data from a file, use the 'read_json' tool. "
    "If the user refers to 'those users' from a previous request, ask them to specify the details again."
)

agent = create_agent(model=llm, tools=TOOLS, system_prompt=SYSTEM_MSG)

def run_agent(user_input: str, history: List[BaseMessage]) -> AIMessage:
    """Single-turn agent runner with automatic tool execution via LangGraph."""
    try:
        result = agent.invoke(
            {"messages": history + [HumanMessage(content=user_input)]},
            config={"recursion_limit": 50}
        )
        return result["messages"][-1]
    except Exception as e:
        return AIMessage(content=f"Error during agent execution: {str(e)}")

if __name__ == "__main__":
    conversation_history: List[BaseMessage] = []
    while True:
        user_input = input("User: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting...")
            break
        ai_response = run_agent(user_input, conversation_history)
        conversation_history.append(HumanMessage(content=user_input))
        conversation_history.append(ai_response)
        print(f"AI: {ai_response.content}")