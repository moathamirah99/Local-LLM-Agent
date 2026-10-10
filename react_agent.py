import requests
import re
import pandas as pd


system_prompt = '''You are an advanced AI agent that thinks step-by-step. 
You must answer questions by reasoning first, then acting.
You have access to 3 tools:
1. CALCULATE: [equation]
2. SEARCH_FILE: [keyword]
3. READ_DATA: [product_name]

You MUST STRICTLY follow this exact format for every turn:

Thought: [Explain your reasoning step-by-step. What do you need to do?]
Action: [TOOL_NAME]: [input]

... (I will return the Observation to you) ...

If you have the final answer, you MUST use this exact format:
Thought: I now have enough information.
Final Answer: [The final answer to the user]

Example of a multi-step question:
User: What is the price of an apple multiplied by 5?
Thought: I need to find the price of an apple first using the database.
Action: READ_DATA: apple

(System will provide Observation: The price is $10...)

Thought: Now I need to multiply 10 by 5.
Action: CALCULATE: 10 * 5

(System will provide Observation: 50...)

Thought: I have the final result.
Final Answer: The price of 5 apples is $50.'''


def safe_calculator(expression: str):
    if not re.match(r'^[\d\+\-\*\/\(\)\.\s]+$' , expression):
        return "error"
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"error {e}"

def search_file(search_keyword):
    keyword_list = []
    try:
        with open("الشركة الوهمية.txt", "r", encoding="utf-8") as file:
            for line in file:
                if search_keyword.lower() in line.lower():
                    keyword_list.append(line.strip())
        if len(keyword_list) > 0:
            return "\n".join(keyword_list)
        else:
            return "error text file not found"
    except FileNotFoundError:
        return "error text file not found"

def reading_csv(keyword):
    try:
        df = pd.read_csv("/home/acer/test_numpy/التدريب العملي/Untitled 1.csv")
        mask = df['product_name'].str.contains(keyword, case= False, na= False)
        result = df[mask]

        if result.empty:
            return "product not found"
        price = result.iloc[0]['price']
        stock = result.iloc[0]['quantity_in_stock']
        return f"price in {price} and we have {stock} in stock"
    except FileNotFoundError:
        return "error csv file not found"

    

class ConversationMemory:
    def __init__(self):
        self.history = []

    def add_user_messeg(self, text):
        self.history.append({"role": "user", "content": text})

    def add_assistant_messeg(self, text):
        self.history.append({"role": "assistant", "content": text})

    def add_tool_result(self, tool_name, result):
        self.history.append({"role": "system", "content": f"observation from tool [{tool_name}]: {result}"})

    def get_context_string(self):
        return self.history


def prais_ai_response(responce_text):
     final_match = re.search(r'Final Answer:\s*(.+)', responce_text)

     calc_match = re.search(r'Action:\s*CALCULATE:\s*(.+)', responce_text)
     file_match = re.search(r'Action:\s*SEARCH_FILE:\s*(.+)', responce_text)
     csv_match = re.search(r'Action:\s*READ_DATA:\s*(.+)', responce_text)

     if final_match:
         return "FINALE_ANSWER:", final_match.group(1).strip()

     elif calc_match:
         return "CALCULATE:", calc_match.group(1).strip()

     elif file_match:
         return "SERCH_FILE:", file_match.group(1).strip()

     elif csv_match:
         return "READ_DATA", csv_match.group(1).strip()

     else:
         return "ERROR", "No valid format"

memory = ConversationMemory()
memory.history.append({"role": "system", "content": system_prompt})

def run_agent(user_question, max_steps = 5):
    print(f"\n[user_qustion]: {user_question}")

    memory.add_user_messeg(user_question)

    step = 0
    while step < max_steps:
        print(f"\n---tinking step {step + 1}")

        response = requests.post("http://localhost:11434/api/chat",
                                 json= {"model": "llama3.2:1b" , 
                                        "messages" : memory.get_context_string(),
                                         "stream": False })
        ai_response = response.json()['message']['content']
        print(f"[ai]: \n{ai_response}")

        memory.add_assistant_messeg(ai_response)

        command_type, command_val = prais_ai_response(ai_response)

        if command_type == "FINALE_ANSWER:" :
            return f"final answer: {command_val}"

        elif command_type == "CALCULATE:":
            result = safe_calculator(command_val)
            memory.add_tool_result("CALCULATE", result)
            print(f"[tool result]: {result}")

        elif command_type == "SERCH_FILE:":
            result = search_file(command_val)
            memory.add_tool_result("SEARCH_FILE", result)
            print(f"tool result: {result}")

        elif command_type == 'READ_DATA':
            result = reading_csv(command_val)
            memory.add_tool_result("READ_DATA:", result)
            print(f"tool result: {result}")

        elif command_type == "ERROR":
            error_msg = "Please use the exact format: Action: [TOOL]: [input] or Final Answer: [answer]"
            memory.add_tool_result("System_Error", error_msg)
            print(f"[Format Error]: Model hallucinated, forcing correction.")

        step += 1

    return "Agent could not reach a final answer in the allowed steps."

while True:
    q = input("\nAsk the Agent (or 'exit'): ")
    if q.lower() == 'exit':
        break
    
    
    final_result = run_agent(q)
    print("\n====================")
    print(final_result)
    print("====================")