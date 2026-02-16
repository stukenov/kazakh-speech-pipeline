import glob
import json
from openai import OpenAI
from utils import get_api_key

def get_all_json_files(directory):
    json_files = glob.glob(f"{directory}/*.json")
    return json_files

PROMPT = (
    "Бұл аудио, жаңалықтар арнасының транскрипциясынан алынған бір тұтас сөйлем, қазақ тілінде. "
    "Сіздің міндетіңіз маған осы мәтіннің грамматикалық түзетілген нұсқасын жіберу. "
    "Тек мәтінді жібер, басқа сөздерді жазба, уақыт кодтарын міндетті түрде қалдырыңыз. "
    "Бір сөйлем бірнеше сөздерге бөлініп сізге жіберілген "
    "Сондықтан, әр сөздерді ретке келдіргенде, олардың бірін-бірімен мағыналық және грамматикалық байланысы болуы екенін ұмытпаңыз."
    "Жауабын JSON форматта жіберіңіз, өрістер тізімі қазіргі мәтіннен түзетілген нұсқасымен бірдей болады."
)

API_KEY = get_api_key()

def get_openai_response(text, api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content

json_files = get_all_json_files("content/captions/json")
for file_path in json_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        json_content = json.load(file)
        
        # Assuming the JSON content is a list of subtitles
        for subtitle in json_content:
            corrected_text = get_openai_response(subtitle['text'], API_KEY)
            subtitle['text'] = corrected_text
        
        grammar_file_path = f"content/captions/grammar/{file_path.split('/')[-1]}"
        with open(grammar_file_path, 'w', encoding='utf-8') as grammar_file:
            json.dump(json_content, grammar_file, ensure_ascii=False, indent=4)
        print(f"Grammar saved to {grammar_file_path}")
   