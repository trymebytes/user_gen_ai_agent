from typing import List
import json
import os
import random
import string
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
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

