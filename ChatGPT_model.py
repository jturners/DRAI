import os
import openai
import json
import pandas as pd

# PUT YOUR FILE LOCATION FOR openFDA.json
file = "/Users/deven/Documents/openFDA.json"

with open(file) as project_file:    
    data = json.load(project_file)  

df = pd.json_normalize(data)

#number of medicines used from the database
n = 10

query = [
    'brand_name', #openfda
    'product_type',
    'route',
'indications_and_usage',
'dosage_and_administration',
'dosage_forms_and_strengths',
'contraindications',
'warnings_and_cautions',
'adverse_reactions',
'pregnancy',
'nursing_mothers',
'precautions',
'storage_and_handling',
'purpose',
'do_not_use',
'stop_use',
'ask_doctor',
'pregnancy_or_breast_feeding',
'when_using',
'questions',
'information_for_patients'
]

#contains all queries for n medicines
all_inf_dict = {}

for i in range(n):
    inf_dict = {}
    results  = df['results'][0][i]
    result_keys = results.keys()
    print()
    
    for q in query:
        if q == 'product_type' or q == 'route':
            
            if 'openfda' in result_keys:
                if q in results['openfda'].keys():
                    inf_dict[q] = results['openfda'][q][0]
                    
                else: pass
            else: pass
        else:
            
            if q in result_keys:
                inf_dict[q] = results[q][0]
   
    if 'openfda' in result_keys:
        if 'brand_name' in results['openfda'].keys():
            all_inf_dict[results['openfda']['brand_name'][0]] = inf_dict

#first medicine chosen
med1 = all_inf_dict[all_inf_dict.keys()[0]]
#this is a dict containing all the info about med1


openai.organization = "org-6AKIjdbpljcerbhjbd24A2Qz"
# Load your API key from an environment variable

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
# chat_completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": "Hello world"}])


def simplify(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": "Simpify and summarise content given by the user or help user find relevent information of subject",
        }
        ]
    messages.append(prompt)
    response = openai.ChatCompletion.create(
        model=model, temperature=0, messages=messages
    )

    return response.choices[0].message["content"]


# test case
#prompt = {"role": "user", "content": "Meloxicam - Meloxicam is a nonsteroidal anti-inflammatory drug (NSAID) used to relieve the symptoms of arthritis (juvenile rheumatoid arthritis, osteoarthritis, and rheumatoid arthritis), such as inflammation, swelling, stiffness, and joint pain."}
userInput = input('Content to summarise: ')
prompt = {"role": "user", "content": userInput}

response = simplify(prompt)
print(response)
