import requests
print("hi im ollama (type exit to quit)")
memory = []
def lastnumber(long_answer):
    if "Final Answer:" in long_answer:
            parts = long_answer.split("Final Answer:")
            final_number = parts[1].replace("[", "").replace("]", "").strip()
            return final_number
    else:
         return "target not found"
            
while True:
    user_input = input("\n who can i help you today ")
    if user_input == "exit":
        print("good by")
        break

    memory.append(f"user : {user_input}")
    full_convesation = "\n".join(memory)

    response = requests.post('http://localhost:11434/api/generate',
                             json = {
                                 "model" : "llama3.2:1b",
                                 'prompt' : full_convesation,
                                 "stream" : False
                             })
    bot_respons = response.json()['response']
    extarcted_number = lastnumber(bot_respons)
    print(f"ai : {bot_respons}")
    print(bot_respons)
    print(f":{extarcted_number}")
    memory.append(f"ai : {bot_respons}")
