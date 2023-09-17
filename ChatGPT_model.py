import os, json, time
import openai
from write_to_csv import writeToCsv

start = time.time()
file = "first45.json"

with open(file) as project_file:    
    data = json.load(project_file)  

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

def simplify(prompt, model="gpt-4"):
    messages = [
        {
            "role": "system",
            "content": "Summarise the medicinal content given by the user without losing factual and statistical content"
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
            "content": "Help user find relevent information about the given medicine. Provide indications and usage, dosage and administration ,dosage forms and strengths, contraindications,warnings and cautions"
        }
        ]
    messages.append(prompt)
    response = openai.ChatCompletion.create(model=model, temperature=0, messages=messages)
    return response.choices[0].message["content"]

def formatResponse(medicine, GPTSummary, GeneralSummary ):
    return {"Medicine": str(medicine), "Database Summary": str(GPTSummary), "General Summary": str(GeneralSummary)}

def getGeneralSummary(medlist) -> list:

    generalSummaryList = []
    medDescription = ""
    for medicine in medlist:
        name = medicine['substance_name']
        medDescription = getGeneralSearch({"role": "user", "content": f"what is {name}"})
        generalSummaryList.append(medDescription)
        
    return generalSummaryList

def getGPTSummary(medlist, descriptionList):

    GPTSummaryList = []
    for med1 in medlist:
        ultimateSummary = ""
        sumSubSummary = ""
        medDescription = ""
        for category in descriptionList:
            if category in med1:
                name = category.replace('_', ' ')
                description = med1[category]
                if len(description) > 1000:
                    medDescription = simplify({"role": "user", "content": description})
                    sumSubSummary += f'{name}: {medDescription}'
                else:
                    sumSubSummary += f'{name}: {description}'
        ultimateSummary += simplify({"role": "user", "content": sumSubSummary})
        GPTSummaryList.append(ultimateSummary)
        
    return GPTSummaryList

firstN = 2
medlist = data[0: firstN]

dataBasedGPT_data = getGPTSummary(medlist, descriptionList)
generalSummaryList = getGeneralSummary(medlist)

    # with open('output1.txt', 'a') as f:
    #     f.write(sumSubSummary)
    #     f.write(2*"\n")

    # dataBasedGPT_data.append(sumSubSummary)
    
#now we can use medlist and dataBasedGPT_data lists



csv = []

for i, GeneralSummary in enumerate(generalSummaryList):
    csv.append(formatResponse(medlist[i]['substance_name'], dataBasedGPT_data[i], GeneralSummary))

writeToCsv(csv)

end = time.time()
print(end-start)

