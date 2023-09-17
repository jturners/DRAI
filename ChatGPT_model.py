import os, json, time

import openai

from write_to_csv import writeToCsv
# from get_medicine import getMed

file = "first45.json"

with open(file) as project_file:    
    data = json.load(project_file)  

firstN = 10
medlist = data[0: firstN]
#medName = medlist[0]["substance_name"]

descriptionList = ['substance_name',
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


openai.organization = "org-6AKIjdbpljcerbhjbd24A2Qz"
# Load your API key from an environment variable

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
# chat_completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": "Hello world"}])

def simplify(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": "Simplify and summarise the content given by the user"
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
            "content": "Help user find relevent information about the given medicine, with indications and usage, dosage and administration ,dosage forms and strengths, contraindications,warnings and cautions"
        }
        ]
    messages.append(prompt)
    response = openai.ChatCompletion.create(model=model, temperature=0, messages=messages)
    return response.choices[0].message["content"]

# def formatResponse(response, medicine):
#     return {"Medicine": medicine, "Summary": response}

start = time.time()
sumSubSummary = ''
for med1 in medlist:
    medDescription = ''
    for category in descriptionList:
        if category in med1:
            name = category.replace('_', ' ')
            description = med1[category]
            if len(description) > 1000:
                medDescription = simplify({"role": "user", "content": description} )
                sumSubSummary += f'{name}: {medDescription} \n'
            else:
                sumSubSummary += f'{name}: {description} \n'


    with open('output1.txt', 'a') as f:
        f.write(sumSubSummary)
        f.write(2*"\n")

    f.close()
    

end = time.time()
print(end-start)
# print(medDescription)
# first medicine chosen



# test case
#prompt = {"role": "user", "content": "Meloxicam - Meloxicam is a nonsteroidal anti-inflammatory drug (NSAID) used to relieve the symptoms of arthritis (juvenile rheumatoid arthritis, osteoarthritis, and rheumatoid arthritis), such as inflammation, swelling, stiffness, and joint pain."}

# input requests are used for testing purposes
# csv = []
# medicine = input('Medicine ')

# lookUpPrompt = {"role": "user", "content": f"what is {medicine}"}

#medicineName = med1['substance_name']
# lookUpResponse = getGeneralSearch(lookUpPrompt)
# csv.append(formatResponse(lookUpResponse, medicine))

# writeToCsv(csv)



