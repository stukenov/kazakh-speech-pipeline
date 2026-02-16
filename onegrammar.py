import json
from openai import OpenAI
from utils import get_api_key

PROMPT = (
    "Бұл аудио, жаңалықтар арнасының транскрипциясынан алынған мәтін, қазақ тілінде. "
    "Сіздің міндетіңіз маған осы мәтіннің грамматикалық түзетілген нұсқасын жіберу. "
    "Тек мәтінді жібер, басқа сөздерді жазба, уақыт кодтарын міндетті түрде қалдырыңыз. "
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
    
def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_content = json.load(file)
        
        i = 0
        while i < len(json_content):
            batch = []
            while i < len(json_content) and not json_content[i]['text'].strip().endswith(('.','!','?')):
                batch.append(json_content[i])
                i += 1
            if i < len(json_content):  # Add the sentence with the punctuation if it's not the end of the file
                batch.append(json_content[i])
                i += 1
            
            # Convert the batch into a JSON string before sending it to OpenAI
            batch_json = json.dumps(batch, ensure_ascii=False)
            corrected_batch_json = get_openai_response(batch_json, API_KEY)
            
            # Parse the corrected JSON content and update the original json_content
            corrected_batch = json.loads(corrected_batch_json)
            for j, corrected_subtitle in enumerate(corrected_batch):
                batch[j]['text'] = corrected_subtitle['text']
    grammar_file_path = f"content/captions/grammar/{file_path.split('/')[-1]}"
    with open(grammar_file_path, 'w', encoding='utf-8') as grammar_file:
        json.dump(json_content, grammar_file, ensure_ascii=False, indent=4)
    print(f"Grammar saved to {grammar_file_path}")

specific_json_file = "content/captions/json/2MJOhrdfhF0.json"
process_json_file(specific_json_file)