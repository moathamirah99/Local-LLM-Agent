import requests
memory = []

system_promt = '''You are a smart assistant.
 If a user asks you a question that requires a mathematical calculation,
 you are not allowed to calculate it yourself.
 You must write the equation only in this format: CALCULATE: [equation]
 Example: CALCULATE: 1500/7
 I will then provide you with the result so you can complete your answer.'''
memory.append(f"system: {system_promt} ")
def findethelast_equation(ai_replay):
    if "CALCULATE:" in ai_replay:
        splited = ai_replay.split("CALCULATE:")
        equation = splited[1].strip()
        return equation
    else:
        return "equation not found"

def calculate(numbers):
    try:
     result = eval(numbers)
     return str(result)
    except:
    
     return "error"

while True:
   user_input = input("what is your question (type exit quit)")
   if user_input == "exit":
      print("ai : good by")
      break

   memory.append(f"user :{user_input}")
   responce = requests.post("http://localhost:11434/api/generate",json=
                            {'model' :'llama3.2:1b',
                             'prompt': "\n".join(memory),
                             'stream': False})
   ai_responce = responce.json()['response']
   

   ecuation = findethelast_equation(ai_responce)
   if ecuation != "equation not found":
      result = calculate(ecuation)
      print(result)
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
   else:
      print(f"ai: {ai_responce}")
      memory.append(f"ai: {ai_responce}")




