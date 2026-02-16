from transformers import pipeline
import soundfile as sf
import torch
import requests
from io import BytesIO

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
transcriber = pipeline(model="anuragshas/whisper-large-v2-kk", device=device)
response = requests.get("https://speech.qazcorpora.kz/storage/2023/11/02//Bgm9C8sb9jD25YodrEq8lTp4Q0pWk5x9kIITRfVR.wav")
audio_data = BytesIO(response.content)
audio_data, samplerate = sf.read(audio_data)
audio_data = audio_data.astype('float32')
result = transcriber(audio_data)
print(result)

# The model is designed to transcribe audio files. It recognizes Kazakh audio files but responds in English,
# indicating it correctly identifies Kazakh text.
