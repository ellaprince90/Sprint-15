import os
from dotenv import load_dotenv
from openai import OpenAI

# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")
# print(f"Loaded API key: {openai_api_key[:5]}...")


# client = OpenAI(api_key=openai_api_key)

# def ask_gpt4o(prompt):
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content

# if __name__ == "__main__":
#     user_input = input("Ask GPT-4o: ")
#     answer = ask_gpt4o(user_input)
#     print("GPT-4o says:", answer)

class my_bot:
    def __init__(self, memory_file="memory.json"):
        load_dotenv()
        api_key=os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        self.client = OpenAI(api_key=api_key)
        self.memory_file = memory_file
        self.memory = self.load_memory()

        if not self.memory:
            self.memory = [
                {"role": "system", "content": "You are a helpful assistant."}
                ]

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print ("Failed to load memory.")
        return []
    
    def save_memory(self):
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.memory, f, indent =2)
        except Exception as e:
            print ("Failed to save memory")

    def ask (self, prompt:str) -> str:
        self.memory.append({"role":"user", "content": prompt})
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages = self.memory
        )
        answer = response.choices[0].message.content
        self.memory.append ({"role": "assistant", "content": answer})
        self.save_memory()
        return answer
    
if __name__ == "__main__":
    bot = my_bot()
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        response = bot.ask(user_input)
        print ("GPT_4o", response)