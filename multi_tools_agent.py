import requests
import pandas as pd
system_prompt = '''you are a smart ai agent you have to answer all question 
but there is three cases your not allowed to answer them from by yourself
case number 1: any mathamtical qusetion you have to only write the equation in this way, CALCULATE: [equation] 
case number 2: If the user asks you for information contained within a text file (Text file/Document), you must write: SEARCH_FILE: [file_name]
case number 3: if the user ask for dat in a csv file you must write: READ_DATA: [data name]
Important: Only output the tool format and stop. I will provide you with the result.
any question exept these three cases you can answer by youeself'''
memory = []
memory.append(f"system: {system_prompt}")
def findethelast_equation(ai_replay):
    if "CALCULATE:" in ai_replay:
        splited = ai_replay.split("CALCULATE:")
        equation = splited[1].strip()
        return equation
    else:
        return "equation not found"

def calculator_tool(expression: str) -> str:
   try:

    result = eval(expression) 
    return str(result)

   except Exception as e:

    return f"{e}"

def order_search_file(ai_answer):
   
   if "SEARCH_FILE:" in ai_answer:
      splited = ai_answer.split("SEARCH_FILE:")
      keword = splited[1].strip()
      return keword
   else:
      return "not found"

def search_file(search_keyword):
   keword_list = []
   with open("الشكرة الوهمية.txt", "r", encoding="utf-8") as file:
      for line in file:
         if search_keyword.lower() in line.lower():
            keword_list.append(line)
   if len(keword_list) > 0 :
      return "\n".join(keword_list)
   else:
      return "not found"

def order_search_csv(ai_answer):
   
   if "READ_DATA:" in ai_answer:
      splited = ai_answer.split("READ_DATA:")
      keword = splited[1].strip()
      return keword
   else:
      return "not found"
def reading_csv(kewword):
  df = pd.read_csv("/home/acer/test_numpy/التدريب العملي/Untitled 1.csv")
  mask = df['product_name'].str.contains(kewword, case=False, na=False)
  result = df[mask]
  if result.empty:
     return "product not found"
  price = result.iloc[0]['price']
  stock = result.iloc[0]['quantity_in_stock']
  return f"The price is ${price}, and we have {stock} in stock"


while True:
   user_input = input("what is your question ")
   if user_input == "exit":
      print("good by")
      break
   memory.append(f"user: {user_input}")
   responce = requests.post("http://localhost:11434/api/generate",json=
                            {'model' :'llama3.2:1b',
                             'prompt': "\n".join(memory),
                             'stream': False})
   ai_responce = responce.json()['response']
   

   
   ecuation = findethelast_equation(ai_responce)
   search_keyword = order_search_file(ai_responce)
   data_keyword = order_search_csv(ai_responce)
   if ecuation != "equation not found":
      result  = calculator_tool(ecuation)
      print(f"tool result{result}")
      memory.append(f"ai: CALCULATE: {ecuation}")
      memory.append(f"system: The result is {result}. Now provide the final answer.")

      response2 = requests.post('http://localhost:11434/api/generate', json={
                        "model": "llama3.2:1b",
                        "prompt": "\n".join(memory),
                        "stream": False
                    })
      finall_ai_recponce = response2.json()['response']
      print(f"ai : {finall_ai_recponce}")
      memory.append(f"ai: {finall_ai_recponce}")

   elif search_keyword != "not found":
      result = search_file(search_keyword)
      print(f"tool result {search_keyword}")
      

      memory.append(f"ai: SEARCH_FILE: {search_keyword}")
      memory.append(f"system: Here is the information from the file: \n{result}\n Now provide the final answer to the user.")

      response2 = requests.post('http://localhost:11434/api/generate', json={
                        "model": "llama3.2:1b",
                        "prompt": "\n".join(memory),
                        "stream": False
                    })
      finall_ai_recponce = response2.json()['response']
      print(f"ai: {finall_ai_recponce}")
      memory.append(f"ai: {finall_ai_recponce}")

   elif data_keyword != "not found":
      result = reading_csv(data_keyword)
      print(f"result is {result}")

      memory.append(f"ai: READ_DATA: {data_keyword}")
      memory.append(f"system: Here is the information from the file: \n{result}\n Now provide the final answer to the user.")
      response2 = requests.post('http://localhost:11434/api/generate', json={
                              "model": "llama3.2:1b",
                              "prompt": "\n".join(memory),
                              "stream": False
                          })
      finall_ai_recponce = response2.json()['response']
      print(f"ai: {finall_ai_recponce}")
      memory.append(f"ai: {finall_ai_recponce}")

   else:
    print(f"ai: {ai_responce}")
    memory.append(f"ai: {ai_responce}")
      
   
