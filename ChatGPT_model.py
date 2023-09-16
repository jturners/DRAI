import os
import openai


#openai.organization = "org-6AKIjdbpljcerbhjbd24A2Qz"
# Load your API key from an environment variable 

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])

