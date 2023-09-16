import os, json

import openai

from write_to_csv import writeToCsv
from get_medicine import getMed

med1 = getMed(0)
print(med1)
#first medicine chosen

openai.organization = "org-6AKIjdbpljcerbhjbd24A2Qz"
# Load your API key from an environment variable

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
# chat_completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": "Hello world"}])


def simplify(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": "Simpify and summarise content given by the user"
        }
        ]
    messages.append(prompt)
    response = openai.ChatCompletion.create(
        model=model, temperature=0, messages=messages
    )

    return response.choices[0].message["content"]

def getGeneralSearch(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": "Help user find relevent information of content given"
        }
        ]
    messages.append(prompt)
    response = openai.ChatCompletion.create(model=model, temperature=0, messages=messages)
    return response.choices[0].message["content"]

def formatResponse(response, medicine):
    return {"Medicine": medicine, "Summary": response}


# test case
#prompt = {"role": "user", "content": "Meloxicam - Meloxicam is a nonsteroidal anti-inflammatory drug (NSAID) used to relieve the symptoms of arthritis (juvenile rheumatoid arthritis, osteoarthritis, and rheumatoid arthritis), such as inflammation, swelling, stiffness, and joint pain."}

# input requests are used for testing purposes
csv = []
medicine = input('Medicine ')

userInput = input('Content to summarise: ')
summarisePrompt = {"role": "user", "content": userInput}

lookUpPrompt = {"role": "user", "content": f"what is {medicine}"}

summariseResponse = simplify(summarisePrompt)
csv.append(formatResponse(summariseResponse, medicine))

lookUpResponse = getGeneralSearch(lookUpPrompt)
csv.append(formatResponse(lookUpResponse, medicine))


writeToCsv(csv)
