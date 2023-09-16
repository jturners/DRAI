import os
import openai


# openai.organization = "org-6AKIjdbpljcerbhjbd24A2Qz"
# Load your API key from an environment variable

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
# chat_completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": "Hello world"}])


def simplify(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": "Simpify and summarise content given by the user",
        },
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model=model, temperature=0, messages=messages
    )

    return response.choices[0].message["content"]


# test case
prompt = "Meloxicam - Meloxicam is a nonsteroidal anti-inflammatory drug (NSAID) used to relieve the symptoms of arthritis (juvenile rheumatoid arthritis, osteoarthritis, and rheumatoid arthritis), such as inflammation, swelling, stiffness, and joint pain."
response = simplify(prompt)
print(response)
