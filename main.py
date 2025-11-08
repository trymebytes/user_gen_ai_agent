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
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return f"Successfully wrote JSON data to '{filepath}' ({len(json.dumps(data))} characters)."
    except Exception as e:
        return f"Error writing JSON to : {str(e)}"

def read_json(filepath: str) -> str:
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

