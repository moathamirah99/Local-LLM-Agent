# Local AI Agent with Tool Calling (ReAct)

## Overview
This repository contains Python scripts demonstrating how to build an AI agent using a local Large Language Model (Llama 3.2 via Ollama). The agent is designed to understand user queries, reason step-by-step (ReAct prompting), and utilize external tools to provide accurate answers without relying on external APIs.

## Features
- **Local LLM Integration:** Uses `Ollama` to run Llama 3.2 locally, ensuring privacy and offline execution.
- **Custom Tools:**
  - `CALCULATE`: Evaluates mathematical expressions safely.
  - `SEARCH_FILE`: Extracts specific information from a local mock text document.
  - `READ_DATA`: Retrieves product details (price and stock) from a CSV inventory file.
- **ReAct Architecture:** Implements a Reason-and-Act loop allowing the AI to break down complex queries into manageable steps before generating a final answer.

## Technologies Used
- Python
- Ollama (Llama 3.2:1b)
- Pandas (for CSV data manipulation)
- Requests (for local API calls)
